# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20150712_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to=b'static/images', blank=True),
        ),
    ]
