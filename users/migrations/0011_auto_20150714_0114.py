# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_item_sold'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(default=b'no-image.png', upload_to=b'images'),
        ),
        migrations.AlterField(
            model_name='item',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to=b'images', blank=True),
        ),
    ]
