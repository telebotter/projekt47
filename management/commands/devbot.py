from django.core.management.base import BaseCommand, CommandError
from projekt47.models import Game
from projekt47 import telegrambot as bot

class Command(BaseCommand):
    help = 'command um bot ohne ssl über polling zu starten'

    def handle(self, *args, **options):
        bot.devmode()
