# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 17:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_and_reg', '0004_auto_20170126_1905'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='email',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
    ]