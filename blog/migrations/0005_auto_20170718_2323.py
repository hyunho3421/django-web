# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-18 14:23
from __future__ import unicode_literals

from django.db import migrations
import django_summernote.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_summernote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=django_summernote.fields.SummernoteTextField(default=''),
        ),
    ]
