import time
import base64
import logging
import datetime
import wsgiref.handlers

from google.appengine.api import urlfetch
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext import db

from utils.jsonrpc import dumps, ServiceHandler, ServiceMethod, ServiceProxy

from index import *

class RPCService(object):
    @ServiceMethod
    def getServices(self):
        logging.debug("getServices()")

        try:
            services_query = Service.all().filter('deleted = ', False).filter('disabled = ', False).order('-tstamp')

            return map(lambda x: {'key': str(x.key()), 'status': x.status, 'hostname': x.hostname}, services_query)
            
        except:
            return []
        
    @ServiceMethod
    def setService(self, service_data):
        logging.debug("setService(%s)" % service_data)
        
        try:
            service = Service.get(service_data['key'])

            if service_data['status'] != 'dnserr' and service_data['ipstr'] != service.ipstr:
                service_headers = {'Authorization': 'Basic ' + base64.b64encode(service.username + ':' + service.password)}
                service_url = 'https://updates.dnsomatic.com/nic/update?hostname=%s&myip=%s' % (service.services, service_data['ipstr'])

                try:
                    service_query = urlfetch.fetch(service_url, None, 'GET', service_headers)
                    service.ipstr = service_data['ipstr']
                    service_data['status'] = str(service_query.content)
                except:
                    service.ipstr = ''
                    service_data['status'] = '!urlfetch'

            if service_data['status'] == 'nochg':
                service.status = 'good ' + service.ipstr

            if service_data['status'] != service.status:
                service.status = service_data['status']
                result = Result()
                result.service = service
                result.status = service.status
                result.put()

            service.tstamp = datetime.datetime.now()
            service.put()

            memcache.delete(key='feed_'+str(service.key()))

            return True
            
        except:
            return False

class RPCHandler(webapp.RequestHandler):
    def error(self, code):
        self.response.clear()
        self.response.set_status(code)
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.out.write(dumps({'result': None, 'id': '', 'error': {'name': 'ServiceRequestError', 'message': str(code)}}))

    def post(self):
        self.response.clear()
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.out.write(ServiceHandler(RPCService()).handleRequest(self.request.body))

def main():
    application = webapp.WSGIApplication([('/rpc/', RPCHandler)])
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
