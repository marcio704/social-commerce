# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-06 21:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_auto_20170906_2126'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='user',
            new_name='vendor',
        ),
    ]
