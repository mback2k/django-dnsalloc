# -*- coding: utf-8 -*-
from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_fields.fields import EncryptedCharField

class Service(models.Model):
    user = models.ForeignKey(User)
    username = EncryptedCharField(_('Username'), max_length=100, db_index=False)
    password = EncryptedCharField(_('Password'), max_length=100, db_index=False)
    hostname = models.CharField(_('Hostname'), max_length=100)
    services = models.CharField(_('Services'), max_length=100, blank=True, null=True)
    crdate = models.DateTimeField(_('Date created'), auto_now_add=True)
    tstamp = models.DateTimeField(_('Date edited'), auto_now=True)
    update = models.DateTimeField(_('Date updated'), blank=True, null=True)
    enabled = models.BooleanField(_('Enabled'), default=True)
    waiting = models.BooleanField(_('Waiting'), default=True)

    def __unicode__(self):
        return self.hostname

    @property
    def status(self):
        return self.result.status

    @property
    def statusimg(self):
        return self.result.statusimg

    @property
    def host(self):
        return self.result.host

    @property
    def results(self):
        return self.result_set.order_by('-crdate')

    @property
    def result(self):
        if not self.waiting and self.result_set.count():
            return self.result_set.latest('crdate')
        else:
            return Result(service=self, status='waiting')

class Result(models.Model):
    service = models.ForeignKey(Service)
    status = models.CharField(_('Status'), max_length=100)
    host = models.CharField(_('Host'), max_length=15, blank=True, null=True)
    crdate = models.DateTimeField(_('Date created'), auto_now_add=True)
    successful = models.BooleanField(_('Successful'))

    def __unicode__(self):
        return self.status

    @property
    def statusimg(self):
        return self.status.split(' ')[0]
