# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-05 20:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_auto_20160904_1604'),
    ]

    operations = [
        migrations.RenameField(
            model_name='options',
            old_name='virtual_play_rows',
            new_name='virtual_player_rows',
        ),
    ]
