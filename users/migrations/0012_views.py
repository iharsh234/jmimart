# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20150714_0114'),
    ]

    operations = [
        migrations.CreateModel(
            name='Views',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('item', models.ForeignKey(to='users.Item')),
                ('student', models.ForeignKey(to='users.Student')),
            ],
        ),
    ]
