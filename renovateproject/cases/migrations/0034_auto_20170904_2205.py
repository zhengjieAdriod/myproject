# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-04 14:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0033_auto_20170825_1801'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schemeinservice',
            old_name='name',
            new_name='name_it',
        ),
    ]