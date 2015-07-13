# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20150711_2255'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
                ('author', models.CharField(max_length=100, null=True)),
                ('publisher', models.CharField(max_length=100, null=True)),
                ('price', models.DecimalField(default=0, max_digits=5, decimal_places=2)),
                ('image', models.ImageField(default=b'no-image.png', upload_to=b'static/images')),
                ('description', models.TextField(null=True)),
                ('student', models.ForeignKey(to='users.Student')),
            ],
        ),
    ]
