# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-04 08:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('village', models.CharField(max_length=70)),
                ('district', models.CharField(max_length=70)),
                ('created_time', models.DateTimeField(blank=True)),
                ('predict', models.CharField(max_length=70)),
                ('fact', models.CharField(max_length=70)),
                ('start_in', models.CharField(max_length=70)),
                ('protection', models.CharField(max_length=70)),
                ('work_site', models.CharField(max_length=70)),
                ('state', models.CharField(max_length=70)),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='Scheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(max_length=70)),
                ('damage_des', models.CharField(max_length=70)),
                ('measures', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('price', models.PositiveIntegerField(default=0)),
                ('describe', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('tele', models.CharField(max_length=70)),
                ('num', models.PositiveIntegerField(default=0)),
                ('praise', models.CharField(max_length=70)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='scheme',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='cases.Scheme'),
        ),
        migrations.AddField(
            model_name='post',
            name='service',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='cases.Service'),
        ),
        migrations.AddField(
            model_name='post',
            name='worker',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='cases.Worker'),
        ),
    ]