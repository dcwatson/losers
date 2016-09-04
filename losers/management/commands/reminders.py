from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.conf import settings
from losers.models import Player

class Command (BaseCommand):
    def handle(self, *args, **options):
        for player in Player.objects.filter(league__current=True, send_reminders=True):
            msg = "Don't forget to set your picks for the week at https://losers.temp.io/"
            send_mail('Loser League Pick Reminder', msg, settings.DEFAULT_FROM_EMAIL, [player.email])
