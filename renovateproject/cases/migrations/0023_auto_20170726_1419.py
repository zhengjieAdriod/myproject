# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-26 06:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0022_worker_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='password',
            field=models.CharField(blank=True, default='111', max_length=70),
        ),
    ]