# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-15 18:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_auto_20170314_0232'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='maximum_irr_return',
            field=models.PositiveSmallIntegerField(blank=True, default=100),
        ),
        migrations.AddField(
            model_name='contact',
            name='minimum_irr_return',
            field=models.PositiveSmallIntegerField(blank=True, default=0),
        ),
    ]
