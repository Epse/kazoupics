# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-15 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0002_auto_20171115_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blocked_poster',
            name='ip',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='blocked_poster',
            name='name',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
    ]