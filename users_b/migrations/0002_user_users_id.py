# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_b', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='users_id',
            field=models.CharField(default=b'', max_length=b'255'),
        ),
    ]
