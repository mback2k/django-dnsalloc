import socket
import urllib2
import datetime
from celery.decorators import task
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
            status = 'good %s' % host
            
        except socket.gaierror:
            host = None
            status = 'dnserr'
        
        if status != service.status and host:
            try:
                mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
                mgr.add_password(None, 'https://updates.dnsomatic.com/nic/update', service.username, service.password)
                
                result = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(mgr)).open('https://updates.dnsomatic.com/nic/update?hostname=%s&myip=%s' % (service.services, host))
                status = result.read().strip()
                
            except urllib2.HTTPError:
                status = 'badauth'
        
        if status != service.status:
            Result.objects.create(service=service, status=status)
            
        if status != service.status or service.waiting:
            service.enabled = False if status in ['notfqdn', 'nohost', 'numhost', 'abuse', 'badauth', '!donator'] else service.enabled
            service.waiting = False
            service.update = datetime.datetime.now()
            service.save()
        
    except Service.DoesNotExist, e:
        pass
