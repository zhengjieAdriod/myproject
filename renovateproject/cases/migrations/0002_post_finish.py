# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-10 07:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='finish',
            field=models.CharField(blank=True, max_length=70),
        ),
    ]