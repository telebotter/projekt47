
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
'nores': 'Tut mir Leid dieser Charakter verfügt über keine Ressource mit der Abkürzung <code>{}</code>',
'nostatreq': 'Vorraussetzungen für Aktion nicht erfüllt.',
'rules': 'Dies sind die allgemeinen Regeln. Für Details lies auf der <a href="{}">Website</a> nach oder schreibe zum Beispiel <code>/regeln 1</code>\n\n{}',
'ress': '{} verfügt über folgende Ressourcen:\n{}\nBsp: <code>/res MP -4</code> verringert die Manapunkte um 4.',
'resschange': '{}s {} geändert:\n{} -> {}',
'skill': 'Skille deinen Character. Verbleibende Punkte: {}',
'skillgrade': 'Skille deinen Character nach Schulnotensystem (1: Sehr gut bis 6: Ungenügend). Verbleibende Skillpunkte: {}',
'nospleft': 'Keine Punkte mehr verfügbar!',
'statsagain': 'Nochmal Werte Skillen. Verbleibnde Skillpunkte: {}',
'hasmetacard': 'Schreibe <code>/metakarte neu</code> um eine neue Karte zu ziehen.',
'probe': '{emoji} <i>{name} braucht {cstat_sum} Augen um {action} zu bestehen.</i>\nWürfel: {wmoji}\n<b>Ergebnis: {roll_sum}\nProbendifferenz : {diff}</b>',
'probehidden': '{emoji} Geheim: <i>{name} braucht {cstat_sum} Augen um {action} zu bestehen.</i>\nWürfel: {wmoji}\n<b>Ergebnis: {roll_sum}\nProbendifferenz : {diff}</b>',
'askname': 'Wie soll der Charakter heißen? Wähle einen Namen aus den Vorschlägen oder sende mir einen Eigenen.',
'charselected': 'Was möchtest du mit dem Charakter {} anstellen?',
'testprobe': 'Aktion: {action}\nWürfel: {n}\nErgebnisse: {rolls}\nErfordert: {cstats}\nErg Summe: {roll_sum}\nErf Summe: {cstat_sum}\nEinzeln: {each}\nSumme: {all}\nPD Summe: {diff}',
'megaprobe': '1000 Proben in {t:.2f}s\nAktion: {action}\nWürfel: {n}\nSumme: {all_p}%\nEinzeln: {each_p}%',
}

RULES = [
{  # 1
'short': 'Der Spielleiter (SL) hat die oberste Entscheidungsgewalt!',
'long': 'Der Spielleiter (SL) hat die oberste Entscheidungsgewalt! Er bestimmt was passiert. Aus dieser Macht erwächst auch die Verantwortung, den Spielern ein möglichst tolles Spielerlebnis zu bereiten. ',
},{  # 2
'short': 'Aktionen werden der Reihe nach ausgeführt!',
'long': 'Damit jeder Spieler die Gelegenheit erhält seinen Charakter in jeder Situation auszuspielen, können Spieler der Reihe nach (Uhrzeigersinn) ankuendigen, welche Aktionen sie ausführen möchten. Der Spielleiter fordert ggf. dazu auf entsprechende Proben auszuführen. Haben sich alle Spieler geäußert, führt der Spielleiter die Aktionen der NPCs aus. In Situationen in denen es logisch erscheint, dass die Charaktere in unterschiedlicher Reihenfolge agieren, (zB wenn sie mit unterschiedlicher Geschwindigkeit auf ein Ziel zu stürmen) sollte dies entsprechend ausgespielt werden.'
},{  # 3
'short': 'Der Erfolg einer Aktion wird durch Würfeln bestimmt!',
'long': 'Aktionen haengen von drei Basiswerten ab. Um eine Aktion durchzufuehren würfelt der Spieler mit drei Würfeln. Übersteigt die Summe der Augen, die Summe der Werte des Charakters gilt die Probe allgemein als bestanden. Durch besondere Umstände, können Proben durch Ansage des SLs erschwert (-x) oder erleichtert (+x) werden. Dieser Wert wird auf die Wuerfelsumme addiert. Wuerfelt der Spieler nur 5 oder 6, kann der SM einen Bonus aussprechen, zB verdopplung des Schadens eines Angriffs. Nur 1 und 2 hingegen, lässt die Aktion katastrophal scheitern.',
},{  # 4
'short': 'Proben werden nur für gelernte Aktionen geworfen!',
'long': 'Die meisten Addons verfügen über einen Satz von (Basis-)Aktionen, die jedem Charakter zur Verfügung stehen. Darüber hinaus, können weitere (Spezial-)Aktionen gelernt werden. Soll der Charakter etwas tun, wofür er keine passende Aktion zur auswahl hat, kann der SL eine alternative Aktion oder ein Basiswert als erschwerte Probe zulassen.',
},{  # 5
'short': 'Eigenverantwortliches Rollenspiel!',
'long': 'Da die Regeln abstrakt und Aktionen oder Werte unterschiedlich starken einfluss auf das Spiel haben können, liegt ein Teil der Verantworung für ein ausgeglichenes Rollenspielerlebnis bei dem Spieler. Sehr abstrakt formulierte Aktionen wie <i>Projektilzauber</i> sollten vom Spieler für ihren Charakter konkretisiert werden, ohne das sie zu stark oder nutzlos werden. Werte und Aktionen sollten so gewählt werden, dass sie am besten zur Geschichte oder zum Charakter passen und nicht um die Warscheinlichkeit zum Gelingen von Proben zu maximieren.',
},{  # 6
'short': 'Aktionen können Ressourcen verbrauchen!',
'long': 'Das Spiel bietet ein sehr vereinfachtes Ressourcensystem. Ob und wie weit dies genutzt wird, oder es dem Spieler überlassen ist, sein Geld oder Leben im Blick zu halten, hängt vom Addon ab. Prinzipiell kann für jede Aktion für den Erfolgs- sowie Misserfolgsfall Kosten (Ressource + Wert) eingetragen werden. Der Wert ist fest, kann aber auch negativ sein, um durch Aktionen (zB Meditieren) Ressourcen wieder aufzufüllen. Sollten der Maximalwert über- oder 0 unterschritten werden, wird der Spieler benachrichtigt und der Wert auf die Grenze gesetzt. Da nicht nur Aktionen die Ressourcen beeinflussen, oder diese in bestimmten Fällen anders kosten, können Ressourcen auch manuell angepasst werden. (/res <abbr> und Nullkosten Feld bei den Proben).'
}
]
