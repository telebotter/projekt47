from django.shortcuts import render
from django.shortcuts import get_list_or_404, get_object_or_404
from django.utils.html import format_html
from projekt47.models import *
from projekt47.constants import *
from django.contrib import messages

def login_hint(request, text=""):
    msg = f'<a href="/login?next={request.path}">Melde dich an</a>{text}'
    if not request.user.is_authenticated:
        messages.info(request, format_html(msg))

# Create your views here.
def index(request):
    context = {}
    return render(request, 'projekt47/index.html', context)


def addons(request):
    context = {}
    context['addons'] = Addon.objects.all()
    login_hint(request, ', um eigene Addons zu erstellen oder zu bearbeiten.')
    return render(request, 'projekt47/addons.html', context)


def addon(request, addon_id):
    context = {}
    context['addon'] = get_object_or_404(Addon, pk=addon_id)
    login_hint(request, ', um eigene Addons zu erstellen oder zu bearbeiten.')
    return render(request, 'projekt47/addon.html', context)


def rules(request):
    context = {'rules': RULES}
    return render(request, 'projekt47/rules.html', context)


def characters(request):
    context = {}
    context['characters'] = Character.objects.all()
    login_hint(request, ', um Charaktere zu erstellen oder zu bearbeiten.')
    return render(request, 'projekt47/characters.html', context)


def character(request, char_id):
    context = {}
    char = get_object_or_404(Character, pk=char_id)
    context['character'] = char
    login_hint(request, ', um Charaktere zu erstellen oder zu bearbeiten.')
    return render(request, 'projekt47/character.html', context)


def adventure(request, adv_id):
    adv = get_object_or_404(Adventure, pk=adv_id)
    context = {'adv': adv}
    login_hint(request,  ', um Abenteuer zu erstellen oder zu bearbeiten.')
    adv = Adventure.objects.get(pk)
