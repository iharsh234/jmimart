# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_item_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(default=0, max_digits=6, decimal_places=2),
        ),
    ]
