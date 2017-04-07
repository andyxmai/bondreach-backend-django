# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-07 04:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0006_correspondence_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='investment_type',
            field=models.CharField(blank=True, choices=[('EQUITY', 'equity'), ('DEBT', 'debt')], max_length=100),
        ),
    ]
