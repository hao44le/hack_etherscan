# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 17:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_topetherdeltatransaction_is_buyer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='etherdeltadailystat',
            old_name='avg_price',
            new_name='avg_buy_price',
        ),
        migrations.AddField(
            model_name='etherdeltadailystat',
            name='avg_sell_price',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]
