# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Amount',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date', models.DateField()),
                ('done', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(null=True, max_length=254, blank=True)),
                ('user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('quantity', models.FloatField(default=0)),
                ('max_quantity', models.FloatField(default=0, blank=True, null=True)),
                ('size', models.FloatField()),
                ('upc_code', models.CharField(null=True, max_length=100)),
                ('url', models.CharField(null=True, max_length=255)),
                ('brand', models.ForeignKey(null=True, to='inventory.Brand')),
                ('user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('products', models.ManyToManyField(through='inventory.Amount', to='inventory.Product')),
                ('user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date', models.DateField()),
                ('used', models.FloatField()),
                ('stocked', models.FloatField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='inventory.Product', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='inventory.Service', null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='amount',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='inventory.Product', null=True),
        ),
        migrations.AddField(
            model_name='amount',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='inventory.Service', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('name', 'size', 'user')]),
        ),
    ]
