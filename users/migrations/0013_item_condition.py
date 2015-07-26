# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='condition',
            field=models.CharField(default='new', max_length=10),
            preserve_default=False,
        ),
    ]
