import datetime
import wsgiref.handlers

from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from view import render
from index import *

class Handler(webapp.RequestHandler):
    def get(self, mode = 'list', id = None):
        service = message = None

        if mode == 'status' and id.isdigit():
            service = Service.get_by_id(int(id))
            if service:
                pass
            else:
                message = 'No such service!'

        elif mode == 'switch' and id.isdigit():
            service = Service.get_by_id(int(id))
            if service:
                service.disabled = not(service.disabled)
                service.update = datetime.datetime.now()
                service.put()
                message = 'Switched service %s!' % ('off' if service.disabled else 'on')
            else:
                message = 'No such service!'

        elif mode == 'delete' and id.isdigit():
            service = Service.get_by_id(int(id))
            if service and service.deleted:
                service.delete()
                message = 'Removed service from datastore!'
            elif service:
                service.deleted = True
                service.update = datetime.datetime.now()
                service.put()
                message = 'Deleted service!'
            else:
                message = 'No such service!'

        elif mode == 'prune' and id.isdigit():
            db.delete(Service.all().filter('deleted', True).fetch(int(100)))
            message = 'Pruned deleted services from datastore!'

        limit = self.request.get_range('limit', min_value=20, max_value=200, default=20)
        offset = self.request.get_range('offset', min_value=0, max_value=1000, default=0)

        userdict = {}
        services = Service.all().order('-userid').fetch(limit, offset)

        for x in services:        
            if x.userid in userdict:
                userdict[x.userid].services.append(x)
            else:
                userdict[x.userid] = x.userid
                userdict[x.userid].userid = x.userid.email()
                userdict[x.userid].uniqueid = x.uniqueid
                userdict[x.userid].services = [x]

        template_values = {
            'limit': limit,
            'limitn': limit * -1,
            'offset': offset,
            'count': Service.all().count(),
            'length': len(services),
            'message': message,
            'service': service,
            'users': userdict
        }

        self.response.out.write(render(self.request, 'views/admin.get.html', 'Admin', template_values))
