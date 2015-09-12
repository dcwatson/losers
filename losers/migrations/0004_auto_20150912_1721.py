# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import losers.models


class Migration(migrations.Migration):

    dependencies = [
        ('losers', '0003_remove_pick_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='login',
            name='code',
            field=models.CharField(unique=True, max_length=20, default=losers.models.random_key),
        ),
    ]
