# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-18 07:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0006_firstimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='firstimage',
            name='post',
        ),
        migrations.AddField(
            model_name='post',
            name='first_image',
            field=models.ManyToManyField(blank=True, to='cases.FirstImage'),
        ),
    ]
