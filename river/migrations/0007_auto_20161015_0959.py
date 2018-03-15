# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-15 09:59
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('river', '0006_auto_20160524_0439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proceedingmeta',
            name='parents',
            field=models.ManyToManyField(
                blank=True, db_index=True, related_name='children', to='river.ProceedingMeta', verbose_name='parents'),
        ),
    ]
