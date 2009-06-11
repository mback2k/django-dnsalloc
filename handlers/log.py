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
        limit = self.request.get_range('limit', min_value=20, max_value=200, default=20)
        offset = self.request.get_range('offset', min_value=0, max_value=1000, default=0)

        results = Result.all().order('-tstamp').fetch(limit, offset)

        template_values = {
            'limit': limit,
            'limitn': limit * -1,
            'offset': offset,
            'count': Result.all().count(),
            'length': len(results),
            'results': results
        }

        self.response.out.write(render(self.request, 'views/log.get.html', 'Log', template_values))
