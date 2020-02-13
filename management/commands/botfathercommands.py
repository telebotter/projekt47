from django.core.management.base import BaseCommand, CommandError
from projekt47.commands import commands
import pandas as pd
from projekt47 import telegrambot as bot
from django.contrib.staticfiles import finders
import os

class Command(BaseCommand):
    help = 'remove all unfinished chars'

    def handle(self, *args, **options):
        text = ''
        for c in commands:
            text += c.aliases[0] + ' - ' + c.text + '\n'
        print(text)
