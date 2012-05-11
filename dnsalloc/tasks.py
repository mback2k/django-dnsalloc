import socket
import urllib2
import datetime
from celery.task import task
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from dnsalloc.models import Service, Result

@task()
def task_start_worker():
    for service in Service.objects.filter(enabled=True):
        task_update_service.apply_async(args=[service.id])

@task()
def task_update_service(service_id):
    try:
        service = Service.objects.get(id=service_id)

        if not service.enabled:
            return

        try:
            host = socket.gethostbyname(service.hostname)

        except socket.gaierror:
            host = None

        if service.waiting or service.host != host:
            if host:
                try:
                    mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
                    mgr.add_password(None, 'https://updates.dnsomatic.com/nic/update', service.username, service.password)

                    result = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(mgr)).open('https://updates.dnsomatic.com/nic/update?hostname=%s&myip=%s' % (service.services, host))
                    status = result.read().strip()

                except urllib2.HTTPError, e:
                    status = 'badauth' if e.code == 401 else 'httperr %d' % e.code

            else:
                status = 'dnserr'

        else:
            status = service.status

        if service.waiting or service.status != status:
            service.enabled = False if status in ['notfqdn', 'nohost', 'numhost', 'abuse', 'badauth', '!donator'] else service.enabled
            service.waiting = False
            service.update = timezone.now()
            service.save()

            Result.objects.create(service=service, status=status, host=host, successful=service.enabled)

        if not service.enabled:
            current_site = Site.objects.get_current()
            edit_service = 'https://%s%s' % (current_site.domain, reverse('dnsalloc.views.edit_service', kwargs={'service_id': service.id}))

            service.user.email_user('DNS Allocator - Update failure for %s - Action required!' % service.hostname,
                                    'DNS Allocator tried to update your host "%s", but failed to do so, because of the following error code:\n\n' \
                                    '%s\n\n' \
                                    'Please go to %s and update your configuration!' % (service.hostname, status, edit_service))

    except Service.DoesNotExist, e:
        pass
