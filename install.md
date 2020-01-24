# Installation einer Testumgebung

```
git clone git@github.com:telebotter/projekt47.git
conda create telebotter python=3.6.8 pip
conda activate telebotter
pip install -r projekt47/requirements.txt
```

## DB configuration
TODO: push migrations wenn remote db verwendet werden soll.. 
projekt47/projekt47/settings.py mit eigenen bot tokens, pfaden und db logins versehen

## db initialisieren

## bot in pollmode und django standalone script 
(import django.settings, bypass django-telegram-bot, setup django env)
telegram bot mit if __name__ funktion starten möglich ohne dass es mit django-telegram-bot main() kollidiert?
