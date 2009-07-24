# -*- coding: utf-8 -*-
from google.appengine.ext import db
from dnsalloc.decorators import cache_property
from django.db.models import signals
from ragendja.dbutils import cleanup_relations

class Service(db.Model):
    user = db.UserProperty()
    userid = db.StringProperty()
    username = db.TextProperty()
    password = db.TextProperty()
    hostname = db.StringProperty()
    services = db.StringProperty()
    crdate = db.DateTimeProperty(auto_now_add=True)
    tstamp = db.DateTimeProperty(auto_now=True)
    update = db.DateTimeProperty()
    enabled = db.BooleanProperty(default=True)
    waiting = db.BooleanProperty(default=True)
    
    def __repr__(self):
        return self.hostname
        
    @cache_property
    def status(self):
        return self.result.status
        
    @cache_property
    def statusimg(self):
        return self.result.statusimg
        
    @cache_property
    def results(self):
        return self.result_set.order('-crdate').fetch(10)
        
    @cache_property
    def result(self):
        if not self.waiting and self.result_set.count():
            return self.result_set.order('-crdate').get()
        else:
            return Result(service=self, status='waiting')

class Result(db.Model):
    service = db.ReferenceProperty(Service)
    status = db.StringProperty()
    crdate = db.DateTimeProperty(auto_now_add=True)
    
    def __repr__(self):
        return self.status
        
    @cache_property
    def statusimg(self):
        return self.status.split(' ')[0]

signals.pre_delete.connect(cleanup_relations, sender=Service)
