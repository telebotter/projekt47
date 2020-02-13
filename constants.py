
# dont slice the string, an emoji can be more than one char (use lists)
EMOJ_NUM = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']


URL = 'https://telebotter.sarbot.de/projekt47/'
URLS = {
    'rules': URL + 'regeln/',
    'addons': URL + 'addons/',
    'abenteuer': URL + 'abenteuer/',
    'help': URL + 'hilfe/'
}

BTN = {
'back': '🔙 zurueck',
'next': 'weiter',
}

MSG = {
'nochar': 'Du hast keinen Charakter aktiviert.',
}

RULES = [
{ # 1
'short': 'Der Spielleiter (SL) hat die oberste Entscheidungsgewalt!',
'long': (
    'Der Spielleiter (SL) hat die oberste Entscheidungsgewalt! ',
    'Sie/er bestimmt was passiert. Aus dieser Macht erwaechst auch die ',
    'Verantwortung, den Spielern ein moeglichst tolles Spielerlebnis zu ',
    'bereiten. '
    ),
},{ # 2
'sort': 'Aktionen werden der Reihe nach ausgefuehrt!',
'long': (
    'Damit jeder Spieler die Gelegenheit erhaelt seinen Charakter in jeder ',
    'Situation auszuspielen, koennen Spieler der Reihe nach (Uhrzeigersinn) ',
    'ankuendigen, welche Aktionen sie ausfuehren moechten. Der Spielleiter ',
    'fordert ggf. dazu auf entsprechende Proben auszufuehren. Haben sich alle ',
    'Spieler geaeussert, fuehrt der Spielleiter die Aktionen der NPCs aus. ',
    'In Situationen in denen es logisch erscheint, dass die Charaktere ',
    'in unterschiedlicher Reihenfolge agieren, (zB wenn sie mit ',
    'unterschiedlicher Geschwindigkeit auf ein Ziel zu stuermen) sollte dies ',
    'entsprechend ausgespielt werden.'
    )
}]
