from google.appengine.ext import db

from utils import models

class Service(models.MemcachedModel):
    userid = db.UserProperty()
    uniqueid = db.StringProperty()
    services = db.StringProperty()
    hostname = db.StringProperty()
    status = db.StringProperty()
    ipstr = db.StringProperty()
    username = db.StringProperty()
    password = db.StringProperty()
    crdate = db.DateTimeProperty(auto_now_add=True)
    update = db.DateTimeProperty()
    tstamp = db.DateTimeProperty()
    disabled = db.BooleanProperty(default=False)
    deleted = db.BooleanProperty(default=False)
    
    def statusimg(self):
        return self.status.split(' ')[0]
        
    def results(self):
        return Result.all().filter('service = ', self).order('-tstamp').fetch(10)

class Result(models.MemcachedModel):
    service = db.ReferenceProperty(Service)
    status = db.StringProperty()
    tstamp = db.DateTimeProperty(auto_now=True)
    
    def statusimg(self):
        return self.status.split(' ')[0]
