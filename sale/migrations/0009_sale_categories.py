# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0008_sale_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='categories',
            field=models.CharField(default=b'[]', max_length=258),
        ),
    ]
