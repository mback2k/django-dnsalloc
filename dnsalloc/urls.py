# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('dnsalloc.views',
    (r'^$', 'show_home'),
    (r'^dashboard/$', 'show_dashboard'),
    (r'^dashboard/service/create/$', 'create_service'),
    (r'^dashboard/service/(?P<service_id>\d+)/$', 'show_service'),
    (r'^dashboard/service/(?P<service_id>\d+)/edit/$', 'edit_service'),
    (r'^dashboard/service/(?P<service_id>\d+)/switch/$', 'switch_service'),
    (r'^dashboard/service/(?P<service_id>\d+)/force/$', 'force_service'),
    (r'^dashboard/service/(?P<service_id>\d+)/delete/$', 'delete_service'),
    (r'^dashboard/service/(?P<service_id>\d+)/delete/ask/$', 'delete_service_ask'),
    (r'^status/$', 'show_status'),
    (r'^feed/service/(?P<service_id>\d+)/status/$', 'feed_service'),
    (r'^login/$', 'redirect_login')
)

urlpatterns += patterns('dnsalloc.methods',
    (r'^api/restful/results\.(?P<format>\w+)$', 'api_results'),
)
