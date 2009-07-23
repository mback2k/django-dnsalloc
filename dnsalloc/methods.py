import base64
import logging
import datetime
from google.appengine.api import urlfetch
from dnsalloc.models import Service, Result
from jsonrpc.decorators import jsonrpc_function

@jsonrpc_function
def getServices(offset):
    logging.debug('getServices(%s)' % (offset))
    
    return map(lambda x: {'key': str(x.key()), 'hostname': x.hostname}, Service.all().filter('enabled = ', True).fetch(25, offset))

@jsonrpc_function
def setService(key, status, host):
    logging.debug('setService(%s, %s, %s)' % (key, status, host))
    
    service = Service.get(key)
    if service:
        if status != service.status and host:
            try:
                status = urlfetch.fetch('https://updates.dnsomatic.com/nic/update?hostname=%s&myip=%s' % (service.services, host), None, 'GET', {'Authorization': 'Basic ' + base64.b64encode('%s:%s' % (service.username, service.password))}).content
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
        service.update = datetime.datetime.now()
        service.put()
