## Management Commands
Django bietet die Moeglichkeit der `management.py` eigene Befehle hinzuzufuegen. Erstellt werden koennen im Prinzip wiederverwendbare Scripte/Funktionen, in denen direkt alle Konfigurationen und Models der App (also projekt47) zur Verfuegung stehen. So muss man sich nicht um DB verbindungen logging oder aehnliches kuemmern. [Mehr zu djangos management commands..](https://docs.djangoproject.com/en/3.0/howto/custom-management-commands/)


### Lokale DB initialisieren
telebotter env: 
```bash
python manage.py makemigrations projekt47 core
python manage.py migrate
```

### runserver
Startet den django internen webserver zum debuggen und testen.
```bash
python manage.py runserver
```
http://127.0.0.1:8000/admin/ im brwoser oeffnen und ID und PW eingeben
addons hinzufügen (oder namensliste importieren). 

Sollte kein admin account fuers webinterface vorliegen:
```bash
python manage.py createsuperuser
```

### botpolling
Wenn in der `settings.py` polling statt webhook angegeben ist, kann der bot mit
```bash
python manage.py botpolling --username=<botusername>
```
gestartet werden. 

### datadump
Daten fuer diesen Bot (+ Userdaten) aus der Server Datenbank zu exportieren:
```bash
python manage.py dumpdata core projekt47 >> serverdb.json
```
Daten in lokaler installation importieren (db muss vorher leer sein):
```bash
python manage.py loaddata serverdb.json
```

### readnames
```bash
python manage.py readnames
```
Die readnames funktion liest eine csv datei mit namen aus, ueberprueft ob diese fuers jeweilige addon schon in der DB stehen und ergaenzt sie falls nicht. Addonnamen sind hardgecoded, ist eher eine einmalige sache gewesen, aber ist denke ich auch ein gutes Beispiel um drauf aufzubauen.

### cleanchars
```bash
python manage.py cleanchars
```
Loescht alle Charaktere die nicht fertiggestellt wurden

### botfathercommands
```bash
python manage.py botfathercommands
```
Gibt alle Befehle mit Hilfetext aus, sodass sie fuer den botfather copy pasted
werden koennen
