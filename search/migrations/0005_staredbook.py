# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_b', '0003_auto_20160101_2355'),
        ('search', '0004_book_ean_13'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaredBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(to='search.Book')),
                ('user', models.ForeignKey(to='users_b.User')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
