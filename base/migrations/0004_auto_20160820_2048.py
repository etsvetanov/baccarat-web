# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-20 17:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='options',
            name='bet_column',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='options',
            name='debt_column',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='options',
            name='index_column',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='options',
            name='level_column',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='options',
            name='net_column',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='options',
            name='pair_number',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='options',
            name='partner_column',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='options',
            name='play_column',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='options',
            name='result_column',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='options',
            name='rows',
            field=models.CharField(choices=[('RP', 'Real players'), ('VP', 'Virtual players'), ('ALL', 'All players')], default='ALL', max_length=3),
        ),
        migrations.AddField(
            model_name='options',
            name='starting_bet',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='options',
            name='step',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='options',
            name='user',
            field=models.CharField(default='John', max_length=50),
        ),
    ]
