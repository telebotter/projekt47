
# dont slice the string, an emoji can be more than one char (use lists)
EMOJ_NUM = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
# Stages
CHOOSE_ADDON, CREATE_CHARACTER, CHARACTER_NAME, OWN_NAME, BASICS = range(5)
SPECIALS, END, STUPIDNUMBER = (5, 6, 7)
# Callback data
ONE, TWO, THREE, FOUR = range(4)

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
'nochar': 'Du hast keinen Charakter aktiviert. Schreib mir privat: /cm',
'norule': 'Dazu hab ich leider keine Regel gefunden.',
'nores': 'Tut mir Leid dieser Charakter verfügt ueber keine Ressource mit der Abkuerzung <code>{}</code>',
'nostatreq': 'Vorraussetzungen fuer Aktion nicht erfuellt.',
'rules': 'Dies sind die allgemeinen Regeln. Für details lies auf der <a href="{}">Website</a> nach oder schreibe zum Beispiel <code>/regeln 1</code>\n\n{}',
'ress': '{} verfügt ueber folgende Ressourcen:\n{}\nBsp: <code>/res MP -4</code> verringert die Manapunkte um 4.',
'resschange': '{}s {} geändert:\n{} -> {}',
'skill': 'Skille deinen Character. Verbleibende Punkte: {}',
'skillgrade': 'Skille deinen Character nach Schulnotensystem (1: Sehr gut bis 6: Ungenügend). Verbleibende Skillpunkte: {}',
'nospleft': 'Keine Punkte mehr verfuegbar!',
'statsagain': 'Nochmal Werte Skillen. Verbleibnde Skillpunkte: {}',
'hasmetacard': 'Schreibe <code>/metakarte neu</code> um eine neue Karte zu ziehen.',
'probe': '{emoji} <i>{name} braucht {cstat_sum} Augen um {action} zu bestehen.</i>\nWürfel: {wmoji}\n<b>Ergebnis: {roll_sum}\nProbendifferenz : {diff}</b>',
'probehidden': '{emoji} Versteckt: <i>{name} braucht {cstat_sum} Augen um {action} zu bestehen.</i>\nWürfel: {wmoji}\n<b>Ergebnis: {roll_sum}\nProbendifferenz : {diff}</b>',
'askname': 'Wie soll der Charakter heissen? Waehle einen Namen aus den Vorschlaegen, oder sende mir einen eigenen.',
'charselected': 'Was moechtest du mit dem Charakter {} anstellen?',
'testprobe': 'Aktion: {action}\nWuerfel: {n}\nErgebnisse: {rolls}\nErfordert: {cstats}\nErg Summe: {roll_sum}\nErf Summe: {cstat_sum}\nEinzeln: {each}\nSumme: {all}\nPD Summe: {diff}',
'megaprobe': '1000 Proben in {t:.2f}s\nAktion: {action}\nWuerfel: {n}\nSumme: {all_p}%\nEinzeln: {each_p}%',
}

RULES = [
{ # 1
'short': 'Der Spielleiter (SL) hat die oberste Entscheidungsgewalt!',
'long': 'Der Spielleiter (SL) hat die oberste Entscheidungsgewalt! Er bestimmt was passiert. Aus dieser Macht erwächst auch die Verantwortung, den Spielern ein möglichst tolles Spielerlebnis zu bereiten. ',
},{ # 2
'short': 'Aktionen werden der Reihe nach ausgeführt!',
'long': 'Damit jeder Spieler die Gelegenheit erhält seinen Charakter in jeder Situation auszuspielen, können Spieler der Reihe nach (Uhrzeigersinn) ankuendigen, welche Aktionen sie ausführen möchten. Der Spielleiter fordert ggf. dazu auf entsprechende Proben auszuführen. Haben sich alle Spieler geäussert, führt der Spielleiter die Aktionen der NPCs aus. In Situationen in denen es logisch erscheint, dass die Charaktere in unterschiedlicher Reihenfolge agieren, (zB wenn sie mit unterschiedlicher Geschwindigkeit auf ein Ziel zu stürmen) sollte dies entsprechend ausgespielt werden.'
}]
