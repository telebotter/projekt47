# @projekt47bot

[![Kontakt](https://img.shields.io/badge/Telegram-Kontakt-blue)](https://tg.me/projekt47bot)
![language](https://img.shields.io/github/languages/top/telebotter/projekt47)
[![closed issues](https://img.shields.io/github/issues-closed/telebotter/projekt47)](https://github.com/telebotter/projekt47/issues?q=is%3Aissue+is%3Aclosed)
![Website](https://img.shields.io/website?url=https%3A%2F%2Ftelebotter.sarbot.de/projekt47/)


Ein Telegrambot bzw. Toolkit für Textbasierte Rollenspiele, inspiriert von Würfel- und Pen&Paper Spielen, mit anpassbaren Regelwerken. Anleitungen zum Spielen finden sich auf der [Website](https://telebotter.sarbot.de/projekt47/) oder ueber den `/hilfe` Befehl in der [Unterhaltung mit dem Bot](https://tg.me/projekt47bot). Das erstellen von Spielern ist [bisher]( https://github.com/telebotter/projekt47/issues/19) Entwicklern ueber das [Admin-Interface](https://telebotter.sarbot.de/admin/projekt47/) vorbehalten.


## Idee
Entstehen soll ein Framework mit einfachem Regelwerk fuer verschiedene Fantasyspiele, dessen Spielspass von der Kreativitaet und dem Enthusiasmus der Spieler und des Spielleiters abhaengen. Die Regeln, sollen einfach und flexibel bleiben, damit neue Spiele mit neuen Hintergrundgeschichten und Szenarien schnell erstellt werden koennen und ein Spiel ohne viel Vorbereitung seitens der Mitspieler begonnen werden kann.
Dieser Bot soll das zentrale und einzig __erforderliche__ Utensil eines jeden Spiels sein. Daher sollte jeder Spieler waerend des Spiels Zugriff auf einen Telegram haben. Nichts desto trotz ist das Regelwerk so ausgelegt, dass zufaellige Ereignisse mit normalen Wuerfeln (1-6) ausgewuerfelt werden koennen. Die generellen Regeln sowie die Spielinhalte eines Addons (Moegliche Aktionen, Werte und Zusatzregeln) sind dafuer auch als pdf verfuegbar.
Mindestens eine Person, leitet ein Spiel und ist dabei der allwissende Erzaehler. Er hat die Entscheidungsgewalt und ist dafuer verantwortlich die Spieler durch das Abenteuer zu fuehren. Wie das Spiel im Detail verlaeuft haengt aber ebenso von den Einzel- und Gruppenentscheidungen der Spieler ab.
Das Uebergeordnete Regelwerk bestimmt, wie gewuerfelt wird und gibt eine grobe Struktur aus Eigenschaften und Aktionen vor. Welche Eigenschaften ein Charakter haben kann und welche Aktionen ihm zur Auswahl stehen, wird in einem Addon definiert. Ebenfalls wird das Szenario also die Hintergrundgeschichte und der Thematische schwerpunkt des Spiels vom jeweiligen Addon vorgegeben. Auf der Website befindet sich eine [Liste von Addons](https://telebotter.sarbot.de/projekt47/addons/) die bereits in Arbeit sind. Beispiele: Scifi, Medival, Fantasy, Schneeballschlacht. Es wird auch moeglich sein eigene Addons zu erstellen, dies allerdings etwas aufwendiger und erfordert Vorbereitungszeit.
Es gibt ausserdem zu jedem Addon [vorgefertigte Abenteuer](https://telebotter.sarbot.de/projekt47/abenteuer), die der Spielleiter als Inspiration fuer die Gestaltung einer Session nehmen kann.


## Management

[Djangos management commands..](https://docs.djangoproject.com/en/3.0/howto/custom-management-commands/)

[Alle wichtigen commands fuer diesen bot..](https://github.com/telebotter/projekt47/blob/master/docs/management.md)

Haeufig verwendete Befehle:

[Lokale DB tabellen updaten](https://github.com/telebotter/projekt47/blob/master/docs/management.md)

```bash
python manage.py makemigrations
python manage.py migrate
```

[Djangos webserver lokal starten](https://github.com/telebotter/projekt47/blob/master/docs/management.md#runserver)
```bash
python manage.py runserver
```

[Bot im polling mode starten](https://github.com/telebotter/projekt47/blob/master/docs/management.md#botpolling)

```bash
python manage.py botpolling --username=<botusername>
```

[DB ex-/importieren](https://github.com/telebotter/projekt47/blob/master/docs/management.md#datadump)
```bash
python manage.py dumpdata core projekt47 >> serverdb.json
python manage.py loaddata serverdb.json
```
