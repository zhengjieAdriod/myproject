# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-20 10:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0035_auto_20170904_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schemeinservice',
            name='name',
            field=models.CharField(max_length=70),
        ),
    ]
