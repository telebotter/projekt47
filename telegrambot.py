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
from django_telegrambot.apps import DjangoTelegramBot
from projekt47.models import *
import random
import logging
logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def start(bot, update):
    update.message.reply_text('hallo')


def main():
    logger.info("Loading handlers for wuerfeln")
    dp = DjangoTelegramBot.getDispatcher('projekt47bot')
    dp.add_handler(CommandHandler('start', start))
    dp.add_error_handler(error)
