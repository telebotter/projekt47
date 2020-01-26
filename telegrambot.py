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


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def start(bot, update):
    tg_user = update.message.from_user
    p_user = ut.get_p_user(tg_user, update=True)
    update.message.reply_text(f'hallo {p_user.telebot_user.first_name}')


def main():
    logger.info("Loading handlers for wuerfeln")
    dp = DjangoTelegramBot.getDispatcher('projekt47bot')
    dp.add_handler(CommandHandler('start', start))
    dp.add_error_handler(error)


def devmode():
    """ function called by manage.py in an local environment (dev mode)
    """
    # INIT TELEGRAM BOT
    updater = Updater(token=settings.PROJEKT47_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_error_handler(error)
    updater.start_polling()
    logger.info('devmode finish')
