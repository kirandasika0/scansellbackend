# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0006_auto_20160110_1757'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='salenotification',
            options={'ordering': ['-pub_date']},
        ),
    ]
