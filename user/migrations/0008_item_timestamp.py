# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_item_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
