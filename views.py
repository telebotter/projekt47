from django.shortcuts import render
from projekt47.models import *
from projekt47.constants import *


# Create your views here.
def index(request):
    context = {}
    return render(request, 'projekt47/index.html', context)


def addons(request):
    context = {}
    context['addons'] = Addon.objects.all()
    return render(request, 'projekt47/addons.html', context)


def addon(request, addon_id):
    context = {}
    context['addon'] = Addon.objects.get(pk=addon_id)
    return render(request, 'projekt47/addon.html', context)


def rules(request):
    context = {'rules': RULES}
    return render(request, 'projekt47/rules.html', context)


def characters(request):
    context = {}
    context['chars'] = Character.objects.all()
    return render(request, 'projekt47/char_list.html', context)


def character(request, char_id):
    context = {}
    char = Character.objects.get(pk=char_id)
    context['char'] = char
    return render(request, 'projekt47/char.html')
