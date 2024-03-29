# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-12 23:45
from __future__ import unicode_literals

from django.db import migrations, models
import utils.dates
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=utils.dates.utcnow)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]
