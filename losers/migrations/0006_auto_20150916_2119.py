# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('losers', '0005_auto_20150914_2338'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='away_spread',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
        migrations.AddField(
            model_name='game',
            name='home_spread',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
    ]
