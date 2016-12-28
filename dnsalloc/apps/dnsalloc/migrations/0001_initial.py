# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

try:
    from django_fields.fields import EncryptedCharField
except ImportError, e:
    from django.db.models import CharField as EncryptedCharField

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=100, verbose_name='Status')),
                ('host', models.CharField(max_length=15, null=True, verbose_name='Host', blank=True)),
                ('crdate', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('successful', models.BooleanField(verbose_name='Successful')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', EncryptedCharField(max_length=100, verbose_name='Username')),
                ('password', EncryptedCharField(max_length=100, verbose_name='Password')),
                ('hostname', models.CharField(max_length=100, verbose_name='Hostname')),
                ('services', models.CharField(max_length=100, null=True, verbose_name='Services', blank=True)),
                ('crdate', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('tstamp', models.DateTimeField(auto_now=True, verbose_name='Date edited')),
                ('update', models.DateTimeField(null=True, verbose_name='Date updated', blank=True)),
                ('enabled', models.BooleanField(default=True, verbose_name='Enabled')),
                ('waiting', models.BooleanField(default=True, verbose_name='Waiting')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='result',
            name='service',
            field=models.ForeignKey(to='dnsalloc.Service'),
            preserve_default=True,
        ),
    ]
