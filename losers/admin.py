from django.contrib import admin
from .models import Game, League, Player, Pick

class GameAdmin (admin.ModelAdmin):
    list_display = ('eid', 'home_team', 'away_team', 'week', 'game_date', 'spread', 'winner', 'loser')
    ordering = ('-year', 'week', 'eid')

class PlayerInline (admin.TabularInline):
    model = Player
    extra = 0

class LeagueAdmin (admin.ModelAdmin):
    list_display = ('name', 'year', 'current')
    list_editable = ('current',)
    inlines = (PlayerInline,)

class PickAdmin (admin.ModelAdmin):
    list_display = ('player', 'week', 'winner', 'loser')
    list_filter = ('player__league', 'week', 'player')

admin.site.register(Game, GameAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Pick, PickAdmin)
