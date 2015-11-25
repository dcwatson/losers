from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings
from losers.models import Team, Game
import requests
import datetime
import decimal
import drill
import time
import pytz

SCORESTRIP_URL = 'http://www.nfl.com/liveupdate/scorestrip/ss.xml?random=%s'
LINE_URL = 'http://xml.pinnaclesports.com/pinnaclefeed.aspx?sporttype=football&sportsubtype=nfl'

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
            # The feed does not specify AM/PM, so I just assume most games are PM. Not the case for some situations,
            # like the games in the UK (9:30 AM EST), but oh well.
            if hour < 12:
                hour += 12
            game_date = game_date.replace(hour=hour, minute=minute)
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
            if game.quarter.startswith('F'):
                game.winner = home if game.home_score > game.away_score else away
                game.loser = home if game.home_score < game.away_score else away
            game.save()
        # Load point spreads
        root = drill.parse(LINE_URL)
        for event in root.find('events/event'):
            game_date = datetime.datetime.strptime(event.event_datetimeGMT.data, '%Y-%m-%d %H:%M')
            game_date = timezone.make_aware(game_date, pytz.utc)
            home = away = ''
            home_spread = away_spread = 0
            for p in event.participants:
                if p.visiting_home_draw.data == 'Home':
                    home = p.participant_name.data.split()[-1].lower()
                elif p.visiting_home_draw.data == 'Visiting':
                    away = p.participant_name.data.split()[-1].lower()
            home_spread = decimal.Decimal(event.periods.period.spread.spread_home.data)
            away_spread = decimal.Decimal(event.periods.period.spread.spread_visiting.data)
            Game.objects.filter(home_team__name=home, away_team__name=away, game_date=game_date).update(home_spread=home_spread, away_spread=away_spread)
