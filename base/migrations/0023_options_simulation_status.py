# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-04 13:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_auto_20161017_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='options',
            name='simulation_status',
            field=models.BooleanField(default=False),
        ),
    ]