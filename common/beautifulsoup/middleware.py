# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.cache import cache
from BeautifulSoup import BeautifulSoup

class BeautifulSoupMiddleware(object):
    def process_response(self, request, response):
        try:
            dump = response.content
        except TypeError:
            return response
        
        if not response.content:
            return response
        
        if not 'Content-Type' in response:
            return response
        
        if not response['Content-Type'].startswith('text/html'):
            return response
        
        if response['Content-Type'].find('charset=') >= 0:
            encoding = response['Content-Type'].split('charset=')[1]
            
        else:
            encoding = settings.DEFAULT_CHARSET
        
        cache_key = 'BeautifulSoup%X' % abs(hash(response.content))
        cache_content = cache.get(cache_key, None)
        
        if cache_content is None:
            response.content = unicode(BeautifulSoup(response.content, fromEncoding=encoding, convertEntities=BeautifulSoup.HTML_ENTITIES))
            cache.set(cache_key, response.content, settings.CACHE_MIDDLEWARE_SECONDS)
            
        else:
            response.content = cache_content

        return response
