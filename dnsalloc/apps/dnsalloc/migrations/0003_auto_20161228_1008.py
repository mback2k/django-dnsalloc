# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dnsalloc', '0002_auto_20140920_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='plain_password',
            field=models.CharField(max_length=100, null=True, verbose_name='Password'),
        ),
        migrations.AddField(
            model_name='service',
            name='plain_username',
            field=models.CharField(max_length=100, null=True, verbose_name='Username'),
        ),
    ]
