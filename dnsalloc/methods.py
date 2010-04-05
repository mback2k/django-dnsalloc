import base64
import datetime
from google.appengine.api import urlfetch
from dnsalloc.models import Service, Result
from jsonrpc.decorators import jsonrpc_function

@jsonrpc_function
def getServices(limit=25, offset=None):
    if offset:
        return Service.objects.all().filter(enabled=True).filter(id__gt=offset).order_by('id')[:limit].values('id', 'hostname')
    else:
        return Service.objects.all().filter(enabled=True).order_by('id')[:limit].values('id', 'hostname')

@jsonrpc_function
def setService(id, status, host):
    try:
        service = Service.objects.get(id=id)
    except Service.DoesNotExist:
        return
        
    if status != service.status and host:
        try:
            status = urlfetch.fetch('https://updates.dnsomatic.com/nic/update?hostname=%s&myip=%s' % (service.services, host), None, 'GET', {'Authorization': 'Basic ' + base64.b64encode('%s:%s' % (service.username, service.password))}).content
        except:
            return
            
    if status != service.status:
        Result.objects.create(service=service, status=status)
        
    service.enabled = False if status in ['dnserr', 'nohost', 'badauth'] else service.enabled
    service.waiting = False
    service.update = datetime.datetime.now()
    service.save()
