# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('losers', '0002_auto_20150912_1813'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pick',
            name='user',
        ),
    ]
