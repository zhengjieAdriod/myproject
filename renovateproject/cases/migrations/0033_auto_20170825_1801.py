# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-25 10:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0032_auto_20170825_1758'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['-created_time']},
        ),
    ]
