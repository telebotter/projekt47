from django.core.management.base import BaseCommand, CommandError
from projekt47.models import DefaultName, Addon
import pandas as pd
from projekt47 import telegrambot as bot
from django.contrib.staticfiles import finders
import os

class Command(BaseCommand):
    help = '(WIP) read csv to db for default names'

    def handle(self, *args, **options):
        #fpath = finders.find('defaultnames.csv')
        fpath = os.path.join('projekt47', 'static', 'projekt47', 'defaultnames.csv')
        data = pd.read_csv(fpath, sep=',')
        addons = {
            'Mittelalter': Addon.objects.get(pk=5)
        }
        for c in data:
            addon = addons[c]
            names = data[c]
            print(addon)
            for n in names:
                dn, new = DefaultName.objects.get_or_create(name=n, addon=addon)
                if new:
                    print('* created *')
            print('done')
