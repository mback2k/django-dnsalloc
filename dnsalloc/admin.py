from django.contrib import admin
from dnsalloc.models import Service, Result

class ServiceAdmin(admin.ModelAdmin):
    fields = ('hostname', 'services', 'enabled')
    list_filter = ('hostname',)
    list_display = ('hostname', 'enabled')
    list_editable = ('hostname', 'enabled')
    date_hierarchy = 'crdate'

class ResultAdmin(admin.ModelAdmin):
    fields = ('service', 'status', 'crdate')
    list_filter = ('service', 'status')
    list_display = ('service', 'status', 'crdate')
    date_hierarchy = 'crdate'

try:
    admin.site.register(Service, ServiceAdmin)
    admin.site.register(Result, ResultAdmin)
except:
    pass
