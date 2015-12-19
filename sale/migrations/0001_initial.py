# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_book_ean_13'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seller_id', models.CharField(max_length=500)),
                ('seller_username', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('price', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(to='search.Book')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SaleImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_name', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('sale', models.ForeignKey(to='sale.Sale')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='SaleInterest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('interested_user_id', models.CharField(max_length=500)),
                ('interested_username', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sale', models.ForeignKey(to='sale.Sale')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
