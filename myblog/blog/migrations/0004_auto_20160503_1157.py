# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-03 11:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20160503_1157'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'permissions': (('can_view_privatepost', 'Может просматривать приватный пост'),)},
        ),
    ]
