# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from . import views, methods

urlpatterns = patterns('',
    url(r'^$', views.show_home, name='show_home'),
    url(r'^dashboard/$', views.show_dashboard, name='show_dashboard'),
    url(r'^dashboard/service/create/$', views.create_service, name='create_service'),
    url(r'^dashboard/service/(?P<service_id>\d+)/$', views.show_service, name='show_service'),
    url(r'^dashboard/service/(?P<service_id>\d+)/edit/$', views.edit_service, name='edit_service'),
    url(r'^dashboard/service/(?P<service_id>\d+)/switch/$', views.switch_service, name='switch_service'),
    url(r'^dashboard/service/(?P<service_id>\d+)/force/$', views.force_service, name='force_service'),
    url(r'^dashboard/service/(?P<service_id>\d+)/delete/$', views.delete_service, name='delete_service'),
    url(r'^dashboard/service/(?P<service_id>\d+)/delete/ask/$', views.delete_service_ask, name='delete_service_ask'),
    url(r'^status/$', views.show_status, name='show_status'),
    url(r'^feed/service/(?P<service_id>\d+)/status/$', views.feed_service, name='feed_service'),
    url(r'^login/$', views.redirect_login, name='redirect_login')
)

urlpatterns += patterns('',
    url(r'^api/restful/results\.(?P<format>\w+)$', methods.api_results, name='api_results'),
)
