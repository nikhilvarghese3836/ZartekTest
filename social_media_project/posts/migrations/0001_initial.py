# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-07-25 14:02
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('pk_bint_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('images', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'posts',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TagWeight',
            fields=[
                ('pk_bint_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('tag', models.CharField(blank=True, max_length=50, null=True)),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('fk_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='posts.Posts')),
            ],
            options={
                'db_table': 'tagweight',
                'managed': True,
            },
        ),
    ]