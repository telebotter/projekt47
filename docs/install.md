> Vorraussetzung fuer folgende Schritte, ist das das [Telebotterprojekt mit Pythonumgebung](https://github.com/telebotter/telebotter/blob/master/install.md)

## Projekt lokal Klonen

```
cd telebotter
git clone git@github.com:telebotter/projekt47.git
```


## Einstellungen anpassen
In der datei `telebotter/settings.py`
`projekt47` in die `INSTALLED_APPS` eintragen (Kommentar entf.). 
Außerdem eigenen `PROJEKT47_TOKEN` eintragen (ganz unten). 


## DB initialisieren
```
python manage.py makemigrations
python manage.py migrate
```
Sollte eine `lokaldb.sqlite` erzeugen, die Tabellen sollte nicht händisch verändert werden.
Falls die Tabellen für die apps noch nicht automatisch generiert wurden, noch einmal explizit (schadet nicht doppelt):

```
python manage.py makemigrations projekt47 core
python manage.py migrate
```
> Muss wiederholt werden, wenn sich die DB Tabellen veraendern (Bei Aenderung in models.py)

## Django Webserver
Wenn der bot unter polling läuft erstmal nicht direkt nötig, darüber kann aber zB das Django Admin Webinterface auch für die lokale DB verwendet werden.
Wenn die `django-telegram-bot app` nicht verwendet wird, steht auch das webinterface fuer die bots nicht zur Verfuegung. Daher
in der `telebotter/urls.py` die Zeile 
```
# url(r'^', include('django_telegrambot.urls')),
``` 
auskommentieren.
Folgenden Befehl zum generieren einiger css Dateien ausfuehren, damit das Admininterface etwas huebscher wird (falls immernoch haesslich pruefen ob settings.py DEBUG=True ist):
```
python manage.py collectstatic
```
Und einen Administrator fuer die lokale Installation hinzufuegen:
```
django-admin createsuperuser
```
Webserver starten mit
```
python manage.py runserver
```
Und den [Link](localhost:8080) Browser (auf dem selben Geraet) oeffnen.


## Bot starten
Die oberen Schritte waren einmalig, vom Projektordner aus kann der bot von jetzt an immer mit `python manage.py devbot` gestartet werden und er läuft bis er crashed (oder strg+c). Damit die richtige python umgebung genutzt wird, muss diese (falls nicht als default gesetzt) aktiviert sein. Zur sicherheit:

```
conda activate telebotter
python manage.py devbot
```
