# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-20 03:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0014_auto_20170719_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_imag',
            field=models.FileField(blank=True, upload_to='imgs/'),
        ),
        migrations.AlterField(
            model_name='startinimage',
            name='path',
            field=models.FileField(blank=True, upload_to='imgs/'),
        ),
    ]