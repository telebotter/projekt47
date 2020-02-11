from django.core.management.base import BaseCommand, CommandError
from projekt47.models import DefaultName, Addon
import pandas as pd
from projekt47 import telegrambot as bot
from django.contrib.staticfiles import finders

class Command(BaseCommand):
    help = '(WIP) read csv to db for default names'

    def handle(self, *args, **options):
        #fpath = finders.find('defaultnames.csv')
        fpath = '/var/www/vhosts/sarbot.de/telebotter.sarbot.de/telebotter/static/projekt47/defaultnames.csv'
        data = pd.read_csv(fpath, sep=',')
        addons = {
            'Mittelalter': Addon.objects.get(pk=4),
            'Standard': Addon.objects.get(pk=1),
            'Scifi': Addon.objects.get(pk=3)
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
