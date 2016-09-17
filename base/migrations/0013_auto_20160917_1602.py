# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-17 13:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0012_auto_20160905_2338'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='bet_column',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='round',
            name='debt_column',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='round',
            name='index_column',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='round',
            name='level_column',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='round',
            name='net_column',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='round',
            name='partner_column',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='round',
            name='play_column',
            field=models.CharField(max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='round',
            name='result_column',
            field=models.CharField(max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='round',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
