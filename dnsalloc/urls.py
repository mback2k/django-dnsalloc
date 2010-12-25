# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('dnsalloc.views',
    (r'^$', 'show_home'),
    (r'^dashboard/$', 'show_dashboard'),
    (r'^dashboard/create/$', 'create_item'),
    (r'^dashboard/status/(?P<service_id>\d+)/$', 'show_item'),
    (r'^dashboard/edit/(?P<service_id>\d+)/$', 'edit_item'),
    (r'^dashboard/switch/(?P<service_id>\d+)/$', 'switch_item'),
    (r'^dashboard/force/(?P<service_id>\d+)/$', 'force_item'),
    (r'^dashboard/feed/(?P<service_id>\d+)/$', 'feed_item'),
    (r'^dashboard/delete/(?P<service_id>\d+)/$', 'delete_item'),
    (r'^dashboard/delete/(?P<service_id>\d+)/ask/$', 'delete_item_ask'),
    (r'^feed/status/(?P<key>\w+)/$', 'feed_item_key'),
)
