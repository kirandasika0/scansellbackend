# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_b', '0002_user_users_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='users_id',
            new_name='user_id',
        ),
    ]
