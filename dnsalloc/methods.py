import base64
import datetime
from google.appengine.api import urlfetch
from dnsalloc.models import Service, Result
from jsonrpc.decorators import jsonrpc_function

@jsonrpc_function
def getServices():
    return map(lambda x: {'key': str(x.key()), 'hostname': x.hostname, 'status': x.status}, Service.all().filter('disabled = ', False))

@jsonrpc_function
def setService(key, status, ip):
    service = Service.get(key)
    if service:
        if status != service.status and ip:
            try:
                status = urlfetch.fetch('https://updates.dnsomatic.com/nic/update?hostname=%s&myip=%s' % (service.services, ip), None, 'GET', {'Authorization': 'Basic ' + base64.b64encode('%s:%s' % (service.username, service.password))}).content
            except:
                status = '!urlfetch'
        else:
            status = 'dnserr'
        
        if status != service.status:
            result = Result()
            result.service = service
            result.status = status
            result.put()

        service.waiting = False
        service.put()
