# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_threshold'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='interval',
            field=models.IntegerField(default=14, null=True),
        ),
    ]
