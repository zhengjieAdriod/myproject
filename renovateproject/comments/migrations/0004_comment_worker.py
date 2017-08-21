# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-21 02:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0027_service_image'),
        ('comments', '0003_auto_20170802_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cases.Worker'),
        ),
    ]