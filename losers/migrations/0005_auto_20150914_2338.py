# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('losers', '0004_auto_20150912_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='send_reminders',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='game',
            name='quarter',
            field=models.CharField(choices=[('P', 'Pre-Game'), ('F', 'Final'), ('FO', 'Final (Overtime)')], max_length=10),
        ),
    ]
