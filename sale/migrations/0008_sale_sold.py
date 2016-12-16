# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0007_auto_20160111_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='sold',
            field=models.BooleanField(default=False),
        ),
    ]
