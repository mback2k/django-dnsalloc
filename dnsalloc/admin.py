from django.contrib import admin
from dnsalloc.models import Service, Result

class ServiceAdmin(admin.ModelAdmin):
    fields = ('user', 'hostname', 'services', 'enabled')
    list_filter = ('hostname',)
    list_display = ('user', 'hostname', 'services', 'crdate', 'enabled')
    date_hierarchy = 'crdate'

class ResultAdmin(admin.ModelAdmin):
    fields = ('service', 'status', 'crdate')
    list_filter = ('status',)
    list_display = ('status', 'crdate')
    date_hierarchy = 'crdate'
    
try:
    admin.site.register(Service, ServiceAdmin)
    admin.site.register(Result, ResultAdmin)
except:
    pass
