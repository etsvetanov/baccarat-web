# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-17 12:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_auto_20161016_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='name',
            field=models.CharField(default='Jose', max_length=20),
        ),
    ]