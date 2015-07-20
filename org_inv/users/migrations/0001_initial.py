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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('location', models.CharField(null=True, blank=True, max_length=255)),
                ('spa_name', models.CharField(null=True, max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
