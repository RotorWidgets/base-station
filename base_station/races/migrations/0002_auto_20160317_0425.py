# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-17 04:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('races', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heatevent',
            name='trigger',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Gate Trigger'), (1, 'Area Entered Trigger'), (2, 'Area Exit Trigger'), (3, 'Crash Trigger'), (4, 'Land Trigger'), (5, 'Takeoff Trigger')]),
        ),
    ]