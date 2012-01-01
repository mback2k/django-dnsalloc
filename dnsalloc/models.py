# -*- coding: utf-8 -*-
from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User
from dnsalloc.decorators import cache_property
from django.utils.translation import ugettext_lazy as _

class Service(models.Model):
    user = models.ForeignKey(User)
    username = models.CharField(_('username'), max_length=30, blank=True, null=True, db_index=False)
    password = models.CharField(_('password'), max_length=30, blank=True, null=True, db_index=False)
    hostname = models.CharField(_('hostname'), max_length=100)
    services = models.CharField(_('services'), max_length=100, blank=True, null=True)
    crdate = models.DateTimeField(_('date created'), auto_now_add=True)
    tstamp = models.DateTimeField(_('date edited'), auto_now=True)
    update = models.DateTimeField(_('date updated'), blank=True, null=True)
    enabled = models.BooleanField(_('enabled'), default=True)
    waiting = models.BooleanField(_('waiting'), default=True)
    
    def __unicode__(self):
        return self.hostname
        
    @cache_property
    def status(self):
        return self.result.status
        
    @cache_property
    def statusimg(self):
        return self.result.statusimg

    @cache_property
    def host(self):
        return self.result.host

    @cache_property
    def results(self):
        return self.result_set.order_by('-crdate')
        
    @cache_property
    def result(self):
        if not self.waiting and self.result_set.count():
            return self.result_set.latest('crdate')
        else:
            return Result(service=self, status='waiting')

class Result(models.Model):
    service = models.ForeignKey(Service)
    status = models.CharField(_('status'), max_length=100)
    host = models.CharField(_('host'), max_length=15, blank=True, null=True)
    crdate = models.DateTimeField(_('date created'), auto_now_add=True)
    
    def __unicode__(self):
        return self.status
        
    @cache_property
    def statusimg(self):
        return self.status.split(' ')[0]
