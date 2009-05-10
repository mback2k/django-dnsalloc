import datetime
import wsgiref.handlers

from google.appengine.api import memcache
from google.appengine.ext import webapp
from utils import rss
from index import *

class Handler(webapp.RequestHandler):
    def get(self, name, key):
        if name == 'status':
            try:
                service = Service.get(key)
            except:
                service = None
            if service:
                service.feed = memcache.get(key='feed_'+key)
            if service and service.feed:
                self.response.headers['Content-Type'] = 'application/rss+xml; charset=utf-8'
                self.response.out.write(service.feed)
            elif service:
                if service.statusimg() == 'good':
                    service.statusimage = 'accept'
                elif service.statusimg() == 'waiting':
                    service.statusimage = 'clock'
                else:
                    service.statusimage = 'error'

                results_query = Result.all().filter('service = ', service).order('-tstamp')
                results = results_query.fetch(20)

                feed = rss.RSS2(
                    title = 'DNS Allocator - Status Feed: %s' % service.hostname,
                    link = 'http://dnsalloc.appspot.com/dashboard/',
                    image = rss.Image('http://dnsalloc.appspot.com/icons/%s.png' % service.statusimage, 'DNS Allocator - Status Feed: %s' % service.hostname, 'http://dnsalloc.appspot.com/dashboard/'),
                    description = 'Shows the latest IP update results from DNS-O-Matic',
                    lastBuildDate = datetime.datetime.now(),
                    items = []
                )
                feed.atomlink_attrs['href'] = self.request.url
                
                for result in results:
                    feed.items.append(rss.RSSItem(
                        title = result.status,
                        description = '%s: %s' % (service.hostname, result.status),
                        link = 'http://dnsalloc.appspot.com/dashboard/status/%s/#%s' % (service.key().id(), result.key().id()),
                        guid = rss.Guid('http://dnsalloc.appspot.com/dashboard/status/%s/#%s' % (service.key().id(), result.key().id())),
                        pubDate = result.tstamp
                    ))

                service.feed = feed.to_xml('utf-8')
                memcache.add(key='feed_'+key, value=service.feed, time=86400)
                self.response.headers['Content-Type'] = 'application/rss+xml; charset=utf-8'
                self.response.out.write(service.feed)
            else:
                self.redirect('/dashboard/')
        else:
            self.redirect('/')
