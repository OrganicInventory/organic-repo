# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20150709_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
