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

## Django Webserver
Wenn der bot unter polling läuft erstmal nicht direkt nötig, darüber kann aber zB das Django Admin Webinterface auch für die lokale DB verwendet werden.


## Bot starten
Die oberen Schritte waren einmalig, vom `telebotter/` Verzeichnis aus kann der bot von jetzt an immer mit `python manage.py devbot` gestartet werden und er läuft bis er crashed (oder strg+c). Damit die richtige python umgebung genutzt wird, muss diese (falls nicht als default gesetzt) aktiviert sein. Zur sicherheit:

```
conda activate telebotter
python manage.py devbot
```
