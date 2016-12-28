# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dnsalloc', '0006_auto_20161228_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='hostname',
            field=models.CharField(max_length=100, verbose_name='Hostname', db_index=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='username',
            field=models.CharField(max_length=100, verbose_name='Username', db_index=True),
        ),
    ]
