# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-30 10:15
from __future__ import unicode_literals

import collections
from django.db import migrations
import temba.utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('flows', '0153_auto_20180130_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flowrun',
            name='fields',
            field=temba.utils.models.JSONAsTextField(blank=True, help_text='A JSON representation of any custom flow values the user has saved away', null=True, object_pairs_hook=collections.OrderedDict),
        ),
    ]