# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-07-26 04:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20200726_0324'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('pk_bint_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('images', models.ImageField(blank=True, null=True, upload_to='')),
            ],
            options={
                'db_table': 'postimages',
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='posts',
            name='images',
        ),
        migrations.AddField(
            model_name='postimage',
            name='fk_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='posts.Posts'),
        ),
    ]
