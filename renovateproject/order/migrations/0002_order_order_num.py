# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-21 05:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_num',
            field=models.CharField(blank=True, max_length=70),
        ),
    ]