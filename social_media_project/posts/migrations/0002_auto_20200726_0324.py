# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-07-26 03:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]