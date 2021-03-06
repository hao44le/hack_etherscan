# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-15 14:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_account_top_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='top_amount',
        ),
        migrations.RemoveField(
            model_name='account',
            name='top_token_holder',
        ),
        migrations.RemoveField(
            model_name='tokentransaction',
            name='top_transaction',
        ),
        migrations.AddField(
            model_name='toptokenholder',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Account'),
        ),
        migrations.AddField(
            model_name='toptokenholder',
            name='top_amount',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='toptokentransaction',
            name='transaction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.TokenTransaction'),
        ),
    ]
