import datetime
import wsgiref.handlers

from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from view import render
from index import *

class Handler(webapp.RequestHandler):
    def get(self):
        results = memcache.get('results')
        if not results:
            userdict = {}
            results = Result.all().fetch(1000)
            for result in results:
                result.status = result.status.split(' ')[0]
    
                if result.status in userdict:
                    userdict[result.status].number += 1
                else:
                    userdict[result.status] = result
                    userdict[result.status].number = 1
    
            for result in userdict:
                userdict[result].percent = round(float(float(userdict[result].number)/len(results))*100, 2)

            results = sorted(userdict.values(), key=lambda x: x.number, reverse=True)
            memcache.add(key='results', value=results, time=300)

        template_values = {
            'services': Service.all().filter('deleted = ', False).filter('disabled = ', False).order('-tstamp').count(),
            'results': results
        }

        self.response.out.write(render(self.request, 'views/home.get.html', 'Home', template_values))
