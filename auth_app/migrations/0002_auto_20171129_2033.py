# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 20:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(default='name', max_length=30),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='surname',
            field=models.CharField(default='surname', max_length=30),
        ),
    ]
