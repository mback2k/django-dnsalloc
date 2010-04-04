import base64
import datetime
from google.appengine.ext import db
from google.appengine.api import urlfetch
from dnsalloc.models import Service, Result
from jsonrpc.decorators import jsonrpc_function

@jsonrpc_function
def getServices(limit, bookmark=None):
    if isinstance(bookmark, basestring):
        bookmark = db.Key(bookmark)
    else:
        bookmark = db.Key.from_path('\0', '\0')
    
    return map(lambda x: {'key': str(x.key()), 'hostname': x.hostname}, Service.all().filter('enabled = ', True).filter('__key__ > ', bookmark).order('__key__').fetch(limit))

@jsonrpc_function
def setService(key, status, host):
    service = Service.get(key)
    if service:
        if status != service.status and host:
            try:
                status = urlfetch.fetch('https://updates.dnsomatic.com/nic/update?hostname=%s&myip=%s' % (service.services, host), None, 'GET', {'Authorization': 'Basic ' + base64.b64encode('%s:%s' % (service.username, service.password))}).content
            except:
                return
        
        if status != service.status:
            result = Result()
            result.service_id = service.key().id()
            result.status = status
            result.put()

        service.enabled = False if status in ['dnserr', 'nohost', 'badauth'] else service.enabled
        service.waiting = False
        service.update = datetime.datetime.now()
        service.put()
