# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-24 22:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0005_correspondence'),
    ]

    operations = [
        migrations.AddField(
            model_name='correspondence',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]