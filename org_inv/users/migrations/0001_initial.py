# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('location', models.CharField(null=True, blank=True, max_length=255)),
                ('spa_name', models.CharField(null=True, max_length=255)),
                ('phone_number', models.CharField(null=True, max_length=15)),
                ('threshold', models.IntegerField(null=True, default=30)),
                ('interval', models.IntegerField(null=True, default=14)),
                ('user', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
