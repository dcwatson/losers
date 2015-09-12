from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone

QUARTER_CHOICES = (
    ('P', 'Pre-Game'),
    ('F', 'Final'),
)

class Team (models.Model):
    abbreviation = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name.capitalize()

class Game (models.Model):
    eid = models.CharField(max_length=10, unique=True)
    home_team = models.ForeignKey(Team, related_name='home_games')
    away_team = models.ForeignKey(Team, related_name='away_games')
    game_date = models.DateTimeField()
    year = models.IntegerField()
    week = models.IntegerField()
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    quarter = models.CharField(max_length=10, choices=QUARTER_CHOICES)
    winner = models.ForeignKey(Team, null=True, blank=True, related_name='wins')
    loser = models.ForeignKey(Team, null=True, blank=True, related_name='losses')

    class Meta:
        ordering = ('eid',)

    def __str__(self):
        return '%s - %s @ %s' % (self.eid, self.away_team, self.home_team)

    @property
    def sunday(self):
        return self.game_date.isoweekday() == 7

    @property
    def started(self):
        return timezone.now() >= self.game_date

    @property
    def played(self):
        return self.winner and self.loser

    @property
    def score(self):
        if self.home_team == self.winner:
            return '%s-%s' % (self.home_score, self.away_score)
        elif self.away_team == self.winner:
            return '%s-%s' % (self.away_score, self.home_score)
        else:
            return ''

class League (models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    current = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Player (models.Model):
    league = models.ForeignKey(League, related_name='players')
    email = models.EmailField()
    name = models.CharField(max_length=100, blank=True)
    paid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('league', 'email')

    def __str__(self):
        return self.name or self.email

class Pick (models.Model):
    player = models.ForeignKey(Player, related_name='picks')
    week = models.IntegerField()
    winner = models.ForeignKey(Team, related_name='winner_picks')
    loser = models.ForeignKey(Team, related_name='loser_picks')

    class Meta:
        unique_together = (
            ('player', 'winner'),
            ('player', 'loser'),
        )

    @property
    def winner_correct(self):
        return Game.objects.filter(year=self.player.league.year, week=self.week, winner=self.winner).exists()

    @property
    def loser_correct(self):
        return Game.objects.filter(year=self.player.league.year, week=self.week, loser=self.loser).exists()

def random_key():
    return get_random_string(40)

class Login (models.Model):
    code = models.CharField(max_length=40, unique=True, default=random_key)
    email = models.EmailField()
    date_created = models.DateTimeField(default=timezone.now)
