# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import losers.models


class Migration(migrations.Migration):

    dependencies = [
        ('losers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('code', models.CharField(unique=True, default=losers.models.random_key, max_length=40)),
                ('email', models.EmailField(max_length=254)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.RemoveField(
            model_name='pick',
            name='confirmed',
        ),
    ]
