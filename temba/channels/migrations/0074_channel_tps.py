# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 20:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0073_auto_20170623_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='tps',
            field=models.IntegerField(help_text='The max number of messages that will be sent per second', null=True, verbose_name='Maximum Transactions per Second'),
        ),
    ]