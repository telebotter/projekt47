## Projekt lokal Klonen

```
git clone git@github.com:telebotter/telebotter.git
cd telebotter
git clone git@github.com:telebotter/projekt47.git
```

## Python Umgebung

```
conda create telebotter python=3.6.8 pip
conda activate telebotter
pip install -r projekt47/requirements.txt
```

## Einstellungen anpassen
In der datei `telebotter/settings.py`
`projekt47` in die `INSTALLED_APPS` eintragen. 
Außerdem eigenen `BOT_TOKEN` setzen. 


## DB configuration
TODO: push migrations wenn remote db verwendet werden soll.. 
projekt47/projekt47/settings.py mit eigenen bot tokens, pfaden und db logins versehen
NOTE: beispiel einstellungen ohne sensible daten werden ins projekt repo geschoben.

## db initialisieren
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

## Django Webserver
Wenn der bot unter polling läuft erstmal nicht direkt nötig, darüber kann aber zB das Django Admin Webinterface auch für die lokale DB verwendet werden.

## bot in pollmode und django standalone script 
(import django.settings, bypass django-telegram-bot, setup django env)
telegram bot mit if __name__ funktion starten möglich ohne dass es mit django-telegram-bot main() kollidiert?
