# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-24 16:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0002_auto_20160322_0626'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_downvotes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='post_upvotes',
        ),
    ]