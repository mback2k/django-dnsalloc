import time
import urllib
import hashlib
import datetime
import wsgiref.handlers

from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.db import djangoforms
from google.appengine.ext.db.djangoforms import forms
from view import render
from index import *

class ServiceForm(djangoforms.ModelForm):
    hostname = forms.RegexField(widget=forms.TextInput(attrs={'size': 20}), regex=r'^[\.a-zA-Z0-9]+$', label='Hostname', help_text='Type in the hostname you want to resolve. (e.g. myhost.dyndns.org)')
    username = forms.RegexField(widget=forms.TextInput(attrs={'size': 20}), regex=r'^\w+$', label='Username', help_text='Type in your DNS-O-Matic username.')
    password = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'size': 20}), label='Password', help_text='Type in your DNS-O-Matic password.')
    services = forms.RegexField(widget=forms.TextInput(attrs={'size': 20}), regex=r'^[\.a-zA-Z0-9]+$', required=False, initial='all.dnsomatic.com', label='Services', help_text='Type in the list of DNS-O-Matic services. (all.dnsomatic.com or hostnames: eg. FQDNs.)')

    def as_yaml(self):
        return template.render('views/form.yaml.html', {'form': self})

    def as_iui(self):
        return template.render('views/form.iui.html', {'form': self})

    class Meta:
        model = Service
        fields = ['hostname', 'username', 'password', 'services']

class Handler(webapp.RequestHandler):
    def get(self, mode='list', id=0, post=False):
        service = message = None
        addform = ServiceForm()

        if mode == 'add' and post:
            addform = ServiceForm(data=self.request.POST)
            if addform.is_valid():
                service = addform.save(commit=False)
                service.userid = users.get_current_user()
                service.uniqueid = service.userid.user_id()
                service.status = 'waiting'
                service.ipstr = ''
                service.update = datetime.datetime.now()
                service.put()
                addform = ServiceForm()
                id = str(service.key().id())
                mode = 'status'
            else:
                mode = 'add'
                
        elif mode == 'edit' and post:
            try:
                service = Service.get(id)
            except:
                service = None
            if service and service.uniqueid == users.get_current_user().user_id() and not service.deleted:
                service.form = ServiceForm(data=self.request.POST, instance=service)
                if service.form.is_valid():
                    service = service.form.save(commit=False)
                    service.userid = users.get_current_user()
                    service.uniqueid = service.userid.user_id()
                    service.status = 'waiting'
                    service.ipstr = ''
                    service.update = datetime.datetime.now()
                    service.put()
                    id = str(service.key().id())
                    mode = 'status'
                else:
                    mode = 'edit'
            else:
                service = None
                mode = 'list'
                
        if mode == 'status' and id.isdigit():
            service = Service.get_by_id(int(id))
            if service and service.uniqueid == users.get_current_user().user_id() and not service.deleted:
                db.delete(Result.all(keys_only=True).filter('tstamp < ', datetime.datetime.fromtimestamp(time.time()-604800)).fetch(100))
            else:
                message = 'No such service on your Dashboard!'
                
        elif mode == 'edit' and id.isdigit():
            service = Service.get_by_id(int(id))
            if service and service.uniqueid == users.get_current_user().user_id() and not service.deleted:
                service.form = ServiceForm(instance=service)
            else:
                message = 'No such service on your Dashboard!'
                
        elif mode == 'switch' and id.isdigit():
            service = Service.get_by_id(int(id))
            if service and service.uniqueid == users.get_current_user().user_id() and not service.deleted:
                service.disabled = not(service.disabled)
                service.update = datetime.datetime.now()
                service.put()
                message = 'Switched service %s!' % ('off' if service.disabled else 'on')
            else:
                message = 'No such service on your Dashboard!'
                
        elif mode == 'delete' and id.isdigit():
            service = Service.get_by_id(int(id))
            if service and service.uniqueid == users.get_current_user().user_id() and not service.deleted:
                service.deleted = True
                service.update = datetime.datetime.now()
                service.put()
                db.delete(Result.all().filter('service = ', service).fetch(1000))
                message = 'Deleted service from your Dashboard!'
            else:
                message = 'No such service on your Dashboard!'
                
        elif mode == 'force' and id.isdigit():
            service = Service.get_by_id(int(id))
            if service and service.uniqueid == users.get_current_user().user_id() and not service.deleted:
                service.status = 'waiting'
                service.ipstr = ''
                service.update = datetime.datetime.now()
                service.put()
                message = 'The service will be updated on next IP check!'
            else:
                message = 'No such service on your Dashboard!'
                
        elif mode == 'feed' and id.isdigit():
            service = Service.get_by_id(int(id))
            if service and service.uniqueid == users.get_current_user().user_id() and not service.deleted:
                content = template.render('views/dashboard.post.html', {'user': users.get_current_user(), 'target': '/feed/status/%s/' % service.key()})
                return self.response.out.write(content)
            else:
                message = 'No such service on your Dashboard!'

        services = Service.all().filter('uniqueid = ', users.get_current_user().user_id()).filter('deleted = ', False).order('-tstamp').fetch(100)

        for x in services:
            x.form = ServiceForm(data=self.request.POST if post and service and str(x.key()) == str(service.key()) else None, instance=x)

        template_values = {
            'services': services,
            'service': service,
            'message': message,
            'addform': addform,
            'mode': mode
        }

        self.response.out.write(render(self.request, 'views/dashboard.get.html', 'Dashboard', template_values))

    def post(self):
        self.get(self.request.get('mode'), self.request.get('edit'), True)
