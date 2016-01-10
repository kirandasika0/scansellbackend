# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0004_sale_geo_point'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notif_type', models.IntegerField()),
                ('user_id', models.CharField(max_length=b'255')),
                ('user_name', models.CharField(max_length=b'255')),
                ('data', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('sale', models.ForeignKey(to='sale.Sale')),
            ],
            options={
                'ordering': ['pub_date'],
            },
        ),
    ]
