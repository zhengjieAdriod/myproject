# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-21 08:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0018_auto_20170721_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='finishimage',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cases.Post'),
        ),
        migrations.AddField(
            model_name='worksiteimage',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cases.Post'),
        ),
        migrations.AlterField(
            model_name='finishimage',
            name='path',
            field=models.FileField(blank=True, upload_to='media/imgs/'),
        ),
        migrations.AlterField(
            model_name='worksiteimage',
            name='path',
            field=models.FileField(blank=True, upload_to='media/imgs/'),
        ),
    ]
