# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0003_saleimage_img_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='geo_point',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
