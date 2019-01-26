# -*- coding: utf-8 -*-
from celery.schedules import crontab
from celery.task import task, periodic_task
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from .models import Service, Result
import urllib
import socket

@periodic_task(run_every=crontab(minute='2,7,12,17,22,27,32,37,42,47,52,57'), ignore_result=True)
def task_start_worker():
    for service in Service.objects.filter(enabled=True):
        task_query_service.apply_async(args=[service.id], task_id='query-service-%d' % service.id)


@task()
def task_query_service(service_id):
    try:
        service = Service.objects.get(id=service_id, enabled=True)
    except Service.DoesNotExist:
        return

    try:
        host = socket.gethostbyname(service.hostname)
    except socket.gaierror:
        host = None

    task_update_service.apply_async(args=[service.id, host], task_id='update-service-%d' % service.id)


@task()
def task_update_service(service_id, host):
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return

    if service.waiting or service.host != host:
        if host:
            try:
                mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
                mgr.add_password(None, 'https://updates.dnsomatic.com/nic/update', service.username, service.password)

                opener = urllib.request.build_opener(urllib.request.HTTPBasicAuthHandler(mgr))
                result = opener.open('https://updates.dnsomatic.com/nic/update?hostname=%s&myip=%s' % (service.services, host))
                status = result.read().strip()

            except urllib.request.HTTPError as e:
                status = 'badauth' if e.code == 401 else 'httperr %d' % e.code

        else:
            status = 'dnserr'

    else:
        status = service.status

    task_save_service.apply_async(args=[service.id, host, status], task_id='save-service-%d' % service.id)


@task()
def task_save_service(service_id, host, status):
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return

    if service.waiting or service.status != status:
        service.enabled = False if status in ['notfqdn', 'nohost', 'numhost', 'abuse', 'badauth', '!donator'] else service.enabled
        service.waiting = False
        service.update = timezone.now()
        service.save()

        Result.objects.create(service=service, status=status, host=host, successful=service.enabled)

    if not service.enabled:
        current_site = Site.objects.get_current()
        edit_service = 'https://%s%s' % (current_site.domain, reverse('dnsalloc:edit_service', kwargs={'service_id': service.id}))

        service.user.email_user('DNS Allocator - Update failure for %s - Action required!' % service.hostname,
                                'DNS Allocator tried to update your host "%s", but failed to do so, because of the following error code:\n\n' \
                                '%s\n\n' \
                                'Please go to %s and update your configuration!' % (service.hostname, status, edit_service))
