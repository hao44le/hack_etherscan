# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-23 22:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_token_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='EtherDeltaTokenTrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('price', models.FloatField()),
                ('is_buy', models.BooleanField()),
                ('amount', models.FloatField()),
                ('amount_base', models.FloatField()),
                ('buyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer_account', to='polls.Account')),
                ('seller', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seller_account', to='polls.Account')),
                ('token_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Token')),
            ],
        ),
        migrations.CreateModel(
            name='EtherTransactionHash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tx_hash', models.CharField(max_length=1024, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='etherdeltatokentrade',
            name='tx_hash',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.EtherTransactionHash'),
        ),
    ]
