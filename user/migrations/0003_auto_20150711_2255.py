# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20150711_2144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='book_count',
            new_name='item_count',
        ),
    ]
