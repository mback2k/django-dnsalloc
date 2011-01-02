import urllib2
import datetime
from dnsalloc.models import Service, Result
from jsonrpc.decorators import jsonrpc_function

@jsonrpc_function
def getServices(limit=25, offset=None):
    if offset:
        return Service.objects.filter(enabled=True).filter(id__gt=offset).order_by('id')[:limit].values('id', 'hostname')
    else:
        return Service.objects.filter(enabled=True).order_by('id')[:limit].values('id', 'hostname')

@jsonrpc_function
def setService(id, status, host):
    try:
        service = Service.objects.get(id=id)
    except Service.DoesNotExist:
        return
        
    if status != service.status and host:
        try:
            mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            mgr.add_password(None, 'https://updates.dnsomatic.com/nic/update', service.username, service.password)
            res = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(mgr)).open('https://updates.dnsomatic.com/nic/update?hostname=%s&myip=%s' % (service.services, host))
            status = res.read()
        except urllib2.HTTPError:
            status = 'badauth'
        except:
            return
            
    if status != service.status:
        Result.objects.create(service=service, status=status)
        
    if status != service.status or service.waiting:
        service.enabled = False if status in ['dnserr', 'nohost', 'badauth'] else service.enabled
        service.waiting = False
        service.update = datetime.datetime.now()
        service.save()
