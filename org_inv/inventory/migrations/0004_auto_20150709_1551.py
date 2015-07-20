# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20150709_1432'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('name', 'size', 'user')]),
        ),
    ]
