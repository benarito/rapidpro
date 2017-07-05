# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-28 18:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0074_channelsession_output'),
        ('flows', '0109_auto_20170629_0813'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlowSession',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('channels.channelsession',),
        ),
        migrations.AddField(
            model_name='flowrun',
            name='output',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='flow',
            name='feature_flag',
            field=models.BigIntegerField(default=0x7FFFFFFFFFFFFFFF,
                                         help_text='Which features are used in this flow'),
        ),
    ]