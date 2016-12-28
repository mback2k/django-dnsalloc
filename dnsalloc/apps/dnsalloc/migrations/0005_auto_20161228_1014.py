# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dnsalloc', '0004_auto_20161228_1009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='password',
        ),
        migrations.RemoveField(
            model_name='service',
            name='username',
        ),
        migrations.AlterField(
            model_name='service',
            name='plain_password',
            field=models.CharField(max_length=100, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='service',
            name='plain_username',
            field=models.CharField(max_length=100, verbose_name='Username'),
        ),
    ]
