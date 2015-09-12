from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings
from losers.models import Team, Game
import requests
import datetime
import drill
import time
import pytz

SCORESTRIP_URL = 'http://www.nfl.com/liveupdate/scorestrip/ss.xml?random=%s'

class Command (BaseCommand):
    def handle(self, *args, **options):
        t = int(time.time() * 1000)
        r = requests.get(SCORESTRIP_URL % t)
        ss = drill.parse(r.text)
        year = int(ss.gms['y'])
        week = int(ss.gms['w'])
        tz = pytz.timezone('US/Eastern')
        for g in ss.gms.children('g'):
            home, _created = Team.objects.get_or_create(abbreviation=g['h'], defaults={'name': g['hnn']})
            away, _created = Team.objects.get_or_create(abbreviation=g['v'], defaults={'name': g['vnn']})
            game_date = datetime.datetime.strptime(g['eid'][:8], '%Y%m%d')
            hour, minute = [int(p) for p in g['t'].split(':', 1)]
            game_date = game_date.replace(hour=hour + 12, minute=minute)
            game, _created = Game.objects.get_or_create(eid=g['eid'], defaults={
                'home_team': home,
                'away_team': away,
                'year': year,
                'week': week,
                'game_date': timezone.make_aware(game_date, tz),
            })
            game.home_score = int(g['hs'])
            game.away_score = int(g['vs'])
            game.quarter = g['q']
            if game.quarter == 'F':
                game.winner = home if game.home_score > game.away_score else away
                game.loser = home if game.home_score < game.away_score else away
            game.save()
