# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20150712_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='sold',
            field=models.BooleanField(default=False),
        ),
    ]
