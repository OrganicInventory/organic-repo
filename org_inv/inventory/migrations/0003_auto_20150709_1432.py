# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20150708_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='upc_code',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.FloatField(),
        ),
    ]
