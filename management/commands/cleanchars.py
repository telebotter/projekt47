from django.core.management.base import BaseCommand, CommandError
from projekt47.models import DefaultName, Addon, Character
import pandas as pd
from projekt47 import telegrambot as bot
from django.contrib.staticfiles import finders
import os

class Command(BaseCommand):
    help = 'remove all unfinished chars'

    def handle(self, *args, **options):
        # fpath = finders.find('defaultnames.csv')
        Character.objects.filter(finished=False).delete()
