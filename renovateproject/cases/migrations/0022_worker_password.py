# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-26 06:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0021_post_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='password',
            field=models.CharField(blank=True, max_length=70),
        ),
    ]
