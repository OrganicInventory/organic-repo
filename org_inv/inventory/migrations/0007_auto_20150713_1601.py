# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20150713_1557'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='brand',
            new_name='brand_name',
        ),
    ]
