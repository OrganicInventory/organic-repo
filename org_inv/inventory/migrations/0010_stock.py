# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_product_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('date', models.DateField()),
                ('used', models.FloatField()),
                ('stocked', models.FloatField()),
                ('product', models.ForeignKey(to='inventory.Product')),
            ],
        ),
    ]
