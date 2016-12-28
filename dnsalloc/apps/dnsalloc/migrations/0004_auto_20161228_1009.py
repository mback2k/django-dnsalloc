# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def decrypt_fields(apps, schema_editor):
    Service = apps.get_model('dnsalloc', 'Service')
    for service in Service.objects.all():
        service.plain_username = service.username
        service.plain_password = service.password
        service.save(update_fields=('plain_username', 'plain_password'))

class Migration(migrations.Migration):

    dependencies = [
        ('dnsalloc', '0003_auto_20161228_1008'),
    ]

    operations = [
        migrations.RunPython(decrypt_fields),
    ]
