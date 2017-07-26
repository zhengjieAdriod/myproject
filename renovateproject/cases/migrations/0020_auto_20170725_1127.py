# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-25 03:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0019_auto_20170721_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finishimage',
            name='des',
            field=models.CharField(blank=True, default='photo', max_length=70),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_imag',
            field=models.FileField(blank=True, upload_to='media/imgs/'),
        ),
        migrations.AlterField(
            model_name='protectionimage',
            name='des',
            field=models.CharField(blank=True, default='photo', max_length=70),
        ),
        migrations.AlterField(
            model_name='startinimage',
            name='des',
            field=models.CharField(blank=True, default='photo', max_length=70),
        ),
        migrations.AlterField(
            model_name='worksiteimage',
            name='des',
            field=models.CharField(blank=True, default='photo', max_length=70),
        ),
    ]
