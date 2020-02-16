
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
'error': 'Ups, da ist was schief gegangen. Tritt der Fehler erneut auf, gib einem Admin bescheid.',
'nochar': 'Du hast keinen Charakter aktiviert.',
'norule': 'Dazu hab ich leider keine Regel gefunden.',
'nores': 'Tut mir Leid dieser Charakter verfügt ueber keine Ressource mit der Abkuerzung <code>{}</code>',
'rules': 'Dies sind die allgemeinen Regeln. Für details lies auf der <a href="{}">Website</a> nach oder schreibe zum Beispiel <code>/regeln 1</code>\n\n{}',
'ress': '{} verfügt ueber folgende Ressourcen:\n{}\nBsp: <code>/res MP -4</code> verringert die Manapunkte um 4.',
'resschange': '{}s {} geändert:\n{} -> {}',
'hasmetacard': 'Schreibe <code>/metakarte neu</code> um eine neue Karte zu ziehen.'
}

RULES = [
{ # 1
'short': 'Der Spielleiter (SL) hat die oberste Entscheidungsgewalt!',
'long': 'Der Spielleiter (SL) hat die oberste Entscheidungsgewalt! Er bestimmt was passiert. Aus dieser Macht erwächst auch die Verantwortung, den Spielern ein möglichst tolles Spielerlebnis zu bereiten. ',
},{ # 2
'short': 'Aktionen werden der Reihe nach ausgeführt!',
'long': 'Damit jeder Spieler die Gelegenheit erhält seinen Charakter in jeder Situation auszuspielen, können Spieler der Reihe nach (Uhrzeigersinn) ankuendigen, welche Aktionen sie ausführen möchten. Der Spielleiter fordert ggf. dazu auf entsprechende Proben auszuführen. Haben sich alle Spieler geäussert, führt der Spielleiter die Aktionen der NPCs aus. In Situationen in denen es logisch erscheint, dass die Charaktere in unterschiedlicher Reihenfolge agieren, (zB wenn sie mit unterschiedlicher Geschwindigkeit auf ein Ziel zu stürmen) sollte dies entsprechend ausgespielt werden.'
}]
