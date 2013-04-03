# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Service, Result

class ServiceAdmin(admin.ModelAdmin):
    fields = ('user', 'hostname', 'services', 'enabled')
    list_filter = ('enabled',)
    list_display = ('user', 'hostname', 'services', 'crdate', 'tstamp', 'update', 'enabled')
    ordering = ('hostname',)

class ResultAdmin(admin.ModelAdmin):
    fields = ('service', 'status')
    list_display = ('service', 'status', 'crdate')
    ordering = ('crdate',)
    
admin.site.register(Service, ServiceAdmin)
admin.site.register(Result, ResultAdmin)
