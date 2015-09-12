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
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('eid', models.CharField(max_length=10, unique=True)),
                ('game_date', models.DateTimeField()),
                ('year', models.IntegerField()),
                ('week', models.IntegerField()),
                ('home_score', models.IntegerField(default=0)),
                ('away_score', models.IntegerField(default=0)),
                ('quarter', models.CharField(choices=[('P', 'Pre-Game'), ('F', 'Final')], max_length=10)),
            ],
            options={
                'ordering': ('eid',),
            },
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('current', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pick',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('week', models.IntegerField()),
                ('confirmed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('paid', models.BooleanField(default=False)),
                ('league', models.ForeignKey(to='losers.League', related_name='players')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('abbreviation', models.CharField(max_length=3, unique=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='pick',
            name='loser',
            field=models.ForeignKey(to='losers.Team', related_name='loser_picks'),
        ),
        migrations.AddField(
            model_name='pick',
            name='player',
            field=models.ForeignKey(to='losers.Player', related_name='picks'),
        ),
        migrations.AddField(
            model_name='pick',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='picks'),
        ),
        migrations.AddField(
            model_name='pick',
            name='winner',
            field=models.ForeignKey(to='losers.Team', related_name='winner_picks'),
        ),
        migrations.AddField(
            model_name='game',
            name='away_team',
            field=models.ForeignKey(to='losers.Team', related_name='away_games'),
        ),
        migrations.AddField(
            model_name='game',
            name='home_team',
            field=models.ForeignKey(to='losers.Team', related_name='home_games'),
        ),
        migrations.AddField(
            model_name='game',
            name='loser',
            field=models.ForeignKey(null=True, related_name='losses', to='losers.Team', blank=True),
        ),
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(null=True, related_name='wins', to='losers.Team', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([('league', 'email')]),
        ),
        migrations.AlterUniqueTogether(
            name='pick',
            unique_together=set([('player', 'winner'), ('player', 'loser')]),
        ),
    ]
