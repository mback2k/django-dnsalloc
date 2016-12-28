# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dnsalloc', '0005_auto_20161228_1014'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='plain_password',
            new_name='password',
        ),
        migrations.RenameField(
            model_name='service',
            old_name='plain_username',
            new_name='username',
        ),
    ]
