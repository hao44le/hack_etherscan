# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-24 23:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20170924_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='topetherdeltatransaction',
            name='is_buyer',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
