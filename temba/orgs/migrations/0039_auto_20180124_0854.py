# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-24 08:54
from __future__ import unicode_literals

from django.db import migrations
import temba.utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0038_auto_20171124_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='org',
            name='config',
            field=temba.utils.models.JSONAsTextField(default=dict, help_text='More Organization specific configuration', null=True, verbose_name='Configuration'),
        ),
    ]