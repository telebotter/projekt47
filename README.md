# projekt47bot

![language](https://img.shields.io/github/languages/top/telebotter/projekt47)
![closed issues](https://img.shields.io/github/issues-closed/telebotter/projekt47)
![Website](https://img.shields.io/website?url=https%3A%2F%2Ftelebotter.sarbot.de/projekt47/)
![GitHub stars](https://img.shields.io/github/stars/telebotter/projekt47)](https://github.com/telebotter/projekt47/stargazers)


Ein Telegrambot bzw. Toolkit für Textbasierte Rollenspiele, inspiriert von Würfel- und Pen&Paper Spielen, mit anpassbaren Regelwerken. Anleitungen zum Spielen finden sich auf der [Website](https://telebotter.sarbot.de/projekt47/) oder ueber den `/hilfe` Befehl in der [Unterhaltung mit dem Bot](https://tg.me/projekt47bot). Das erstellen von Spielern ist [bisher]( https://github.com/telebotter/projekt47/issues/19) Entwicklern ueber das [Admin-Interface](https://telebotter.sarbot.de/admin/projekt47/) vorbehalten.


## Idee
Entstehen soll ein Framework fuer Regeltechnisch einfache Fantasyspiele, dessen Spielspass von der Kreativitaet und dem Enthusiasmus der Spieler und des Spielleiters abhaengen. Die Regeln, sollen einfach und flexibel bleiben, damit neue Spiele mit neuen Hintergrundgeschichten und Szenarien schnell erstellt werden koennen und ein Spiel ohne viel Vorbereitung seitens der Mitspieler begonnen werden kann.
Dieser Bot soll das zentrale und einzig __erforderliche__ Utensil eines jeden Spiels sein. Daher sollte jeder Spieler waerend des Spiels Zugriff auf einen Telegram haben. Nichts desto trotz ist das Regelwerk so ausgelegt, dass zufaellige Ereignisse mit normalen Wuerfeln (1-6) ausgewuerfelt werden koennen. Die generellen Regeln sowie die Spielinhalte eines Addons (Moegliche Aktionen, Werte und Zusatzregeln) sind dafuer auch als pdf verfuegbar.
Mindestens eine Person, leitet ein Spiel und ist dabei der allwissende Erzaehler. Er hat die Entscheidungsgewalt und ist dafuer verantwortlich die Spieler durch das Abenteuer zu fuehren. Wie das Spiel im Detail verlaeuft haengt aber ebenso von den Einzel- und Gruppenentscheidungen der Spieler ab.
Das Uebergeordnete Regelwerk bestimmt, wie gewuerfelt wird und gibt eine grobe Struktur aus Eigenschaften und Aktionen vor. Welche Eigenschaften ein Charakter haben kann und welche Aktionen ihm zur Auswahl stehen, wird in einem Addon definiert. Ebenfalls wird das Szenario also die Hintergrundgeschichte und der Thematische schwerpunkt des Spiels vom jeweiligen Addon vorgegeben. Auf der Website befindet sich eine [Liste von Addons](https://telebotter.sarbot.de/projekt47/addons/) die bereits in Arbeit sind. Beispiele: Scifi, Medival, Fantasy, Schneeballschlacht. Es wird auch moeglich sein eigene Addons zu erstellen, dies allerdings etwas aufwendiger und erfordert Vorbereitungszeit.
Es gibt ausserdem zu jedem Addon [vorgefertigte Abenteuer](https://telebotter.sarbot.de/projekt47/abenteuer), die der Spielleiter als Inspiration fuer die Gestaltung einer Session nehmen kann.

# Entwicklung

## Management Commands
Django bietet die Moeglichkeit der `management.py` eigene Befehle hinzuzufuegen. Erstellt werden koennen im Prinzip wiederverwendbare Scripte/Funktionen, in denen direkt alle Konfigurationen und Models der App (also projekt47) zur Verfuegung stehen. So muss man sich nicht um DB verbindungen logging oder aehnliches kuemmern. [Mehr zu djangos management commands..](https://docs.djangoproject.com/en/3.0/howto/custom-management-commands/)

### readnames
Die readnames funktion liest eine csv datei mit namen aus, ueberprueft ob diese fuers jeweilige addon schon in der DB stehen und ergaenzt sie falls nicht. Pfade und Addon namen sind hardgecoded, ist eher eine einmalige sache gewesen, aber ist denke ich auch ein gutes Beispiel um drauf aufzubauen.

### cleancharacters
Sucht Chraktere in der Datenbank, die nie fertig gestellt wurden und aelter als 2 Tage sind um sie zu loeschen. #20
