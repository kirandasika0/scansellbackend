# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_auto_20151123_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='ean_13',
            field=models.CharField(default=b'', max_length=300),
        ),
    ]
