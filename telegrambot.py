#myapp/telegrambot.py
# Example code for telegrambot.py module


from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import InlineQueryResultArticle
from telegram import ParseMode
from telegram import InputTextMessageContent
from telegram.ext import CommandHandler
from telegram.ext import InlineQueryHandler
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import Filters
from telegram.ext import Updater  # for devmode
from django_telegrambot.apps import DjangoTelegramBot
from projekt47.models import *
from projekt47 import utils as ut
import random
import logging
from django.conf import settings
logger = logging.getLogger(__name__)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   run the bot
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def start(bot, update):
    tg_user = update.message.from_user
    p_user = ut.get_p_user(tg_user, update=True)
    update.message.reply_text(f'hallo {p_user.telebot_user.first_name}')


def devtest(bot, update):
    update.message.reply_text('Ich bin der pollende test bot')


def webtest(bot, update):
    update.message.reply_text('Ich bin der offizielle web bot')


def sharetest(bot, update):
    update.message.reply_text('Ich bin eine normale antwort')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   run the bot
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def add_shared_handlers(dp):
    """ This function adds handlers that are used in dev (polling) and
    production (webhook). DTB dispatcher is a subclass of the PTB dp, they share
    most of their methods and can be used in a similar way.
    """
    # handlers for both methods
    dp.add_handler(CommandHandler('start', start))
    dp.add_error_handler(error)


def main():
    """ function called by django-telegram-bot automatically on webhook
    """
    dp = DjangoTelegramBot.getDispatcher('projekt47bot')
    add_shared_handlers(dp)
    # add webhook specific handlers below
    dp.add_handler(CommandHandler('webtest', webtest))


def devmode():
    """ function called by manage.py in an local environment (dev mode)
    """
    up = Updater(token=settings.PROJEKT47_TOKEN)
    dp = up.dispatcher
    add_shared_handlers(dp)
    # add polling specific handlers (or under development) below
    dp.add_handler(CommandHandler('devtest', devtest))
    # start the update loop
    up.start_polling()
