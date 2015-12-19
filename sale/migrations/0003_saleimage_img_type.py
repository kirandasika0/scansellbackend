# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0002_sale_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleimage',
            name='img_type',
            field=models.CharField(default=b'', max_length=b'16'),
        ),
    ]
