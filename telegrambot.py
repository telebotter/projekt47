from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import InlineQueryResultArticle
from telegram import ParseMode
from telegram import InputTextMessageContent
from telegram.ext import ConversationHandler
from telegram.ext import CommandHandler
from telegram.ext import InlineQueryHandler
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import Filters
from telegram.ext import Updater  # for devmode
from django_telegrambot.apps import DjangoTelegramBot  # for webmode
from projekt47 import utils as ut
from projekt47.models import *
from uuid import uuid4
import random
import logging
from django.conf import settings
import os
import pwd

# Run when import
logger = logging.getLogger(__name__)
os_user = pwd.getpwuid(os.getuid()).pw_name
logger.debug(f'loading projekt47 module by user: {os_user}')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  character creation / conversation frame
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Stages
CHOOSE_ADDON, CREATE_CHARACTER, CHARACTER_NAME, OWN_NAME, BASICS, SPECIALS, END = range(7)
# Callback data
ONE, TWO, THREE, FOUR = range(4)


def character_menu(bot, update):
    """ entry point for the character select/create menu (cm_ prefix).
    Send message on `/charakter`. Choose character.
    NOTE: renamed from start() to character_menu() and Held to Charakter.
    NOTE: replaced placeholder with DB queries
    """
    logger.debug(f'{update.message.from_user.first_name} started conversation')
    text = 'Waehle einen Helden'
    keyboard = [[InlineKeyboardButton('Neuer Charakter',
                callback_data='cm_newchar')]]
    player = ut.get_p_user(update.message.from_user)
    chars = Character.objects.filter(owner=player)
    for char in chars:
        keyboard.append([
                InlineKeyboardButton(f'{char.name}',
                        callback_data='cm_activate,{char.id}')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text, reply_markup=reply_markup)
    return CHOOSE_ADDON


def cm_choose_addon(bot, update):
    """ Show new options of buttons too choose a addon. This is the first and
    required step to create a new character. The character object is already
    created here.
    # TODO: add date_created and created to char, and use management command
    to clean up from time to time.
    """
    logger.debug(f'choose addon')
    query = update.callback_query
    player = ut.get_p_user(query.from_user)

    # init new character
    logger.warn('creating new char')
    new_char = Character.objects.create(owner=player, name='NEU')
    new_char.save()  # need to be saved to get an ID
    player.active_char = new_char  # keep the reference in this conversation
    player.save()
    addons = Addon.objects.all()
    keyboard = []
    for addon in addons:
        keyboard.append([InlineKeyboardButton(f'{addon.name}',
                                            callback_data=f'cm,{addon.id}')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Wähle ein Spiel",
        reply_markup=reply_markup
    )
    return CREATE_CHARACTER


def cm_name(bot, update):
    """ Saves previous choice (addon).
    Send some suggestions for names or read from user input.
    """
    query = update.callback_query
    player = ut.get_p_user(query.from_user)
    char = player.active_char

    # set players stats and actions and save addon choice
    addon_id = int(query.data.split(',')[1])
    addon = Addon.objects.get(pk=addon_id)
    char.addon = addon
    char.skill_points = addon.skill_points
    for stat in addon.stats.all():
        char.stats.add(stat, through_defaults={'value': 4})
    char.save()

    # next message
    text = 'Wie soll der Charakter heissen? Waehle einen Namen aus den\
Vorschlaegen, oder sende mir einen eigenen.'
    keyboard = [[InlineKeyboardButton('Peter', callback_data='cm,peter')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=text,
        reply_markup=reply_markup
    )
    return BASICS


def cm_stats_custom_name(bot, update):
    """ handles incomming message during name selection state.
    Gather all stats that are available for the selected addon and list them.
    The function has to be called everytime one of the stats change.
    #TODO: track unset stats (freie Skillpunkte).
    """
    logger.warning('custom name message detected')
    text = f'Soll dein Charakter {update.message.text} heissen?'
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Ja!',
                    callback_data=f'cm,{update.message.text}')]])
    update.message.reply_text(text, reply_markup=reply_markup)


def cm_stats(bot, update):
    """Saves previous choice (name).
    Gather all stats that are available for the selected addon and list them.
    The function has to be called everytime one of the stats change.
    #TODO: track unset stats (freie Skillpunkte).
    """
    query = update.callback_query
    player = ut.get_p_user(query.from_user)

    # save choice name
    name = query.data.split(',')[1]
    player.active_char.name = name
    player.active_char.save()


    # next message
    text = f"Skille deinen Character nach Schulnotensystem (1: Sehr gut bis 6: \
Ungenügend). Verbleibende Skillpunkte: {player.active_char.skill_points}"
    keyboard = ut.skill_keyboard(player.active_char)
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text= text,
        reply_markup=reply_markup
    )
    return SPECIALS


def cm_actions(bot, update):
    """ save the stat changes and update the skill keyboard. If cb data contains
    `ok` (stat skill finished), save and post action keyboard instead.
    returning current conversation state (SPECIALS) is like doing nothing.
    """
    query = update.callback_query
    player = ut.get_p_user(query.from_user)
    char = player.active_char
    data = query.data.split(',')

    # handle skill keyboard cb data
    if not data[0] == 'cm':  # ignore unrelated callbacks
        return SPECIALS
    elif data[1] == 'statalert':
        # user pressed the stat name, open description popup and stay in state
        stat = Stat.objects.get(pk=data[2])
        query.answer(text=f'{stat.name} ({stat.abbr}): {stat.text}',
                        show_alert=True)
        return SPECIALS
    elif data[1] == 'skill':
        # user pressed + or -
        char.skill_points += int(data[3])
        if char.skill_points < 0:
            char.skill_points -= int(data[3])
            query.answer('Keine Punkte mehr verfuegbar!')
        char.save()
        cstat = CharStat.objects.get(pk=data[2])
        cstat.value += int(data[3])
        if cstat.value < 1 or cstat.value > 5:
            # return without saving or updating the keyboard
            query.answer('Nur Werte von 1-6 erlaubt!')
            return SPECIALS
        cstat.save()
        # update message:
        markup = InlineKeyboardMarkup(ut.skill_keyboard(player.active_char))
        bot.edit_message_text(chat_id=query.message.chat_id,
                            message_id=query.message.message_id,
                            text=f"Skille deinen Character. Verbleibende \
                                Punkte: {char.skill_points}",
                            reply_markup=markup)
        return SPECIALS  # stay in skill state
    elif data[1] == 'finish':
        keyboard = ut.action_keyboard(player.active_char)
        reply_markup= InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=f"Skille deinen Character. Verbleibende Punkte: \
                {char.skill_points}",
            reply_markup=reply_markup
        )
        return END
    logger.warning('unhandled callback in cm_actions')
    return SPECIALS


def cm_end(bot, update):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over
    TODO: loop the action skill keyboard until finish is pressed
    """
    query = update.callback_query
    data = query.data.split(',')
    player = ut.get_p_user(query.from_user)
    char = player.active_char
    if data[1] == 'skillaction':
        new_action = Action.objects.get(pk=data[2])
        if char.skill_points < 1:
            query.answer("Keine Punkte mehr uebrig!")
            return END
        char.skill_points -= 1
        char.actions.add(new_action)
        char.save()
        # repost updated keyboard:
        keyboard = ut.action_keyboard(player.active_char)
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = f"Skille deinen Character. Verbleibende Punkte: {char.skill_points}"
        for act in player.active_char.actions.all():
            text += f'\n  {act.name}'
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=text,
            reply_markup=reply_markup
        )
        return END
    elif data[1] == 'finish':
        player.active_char.finished = True
        player.active_char.save()
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=f"<b>{char.name}</b> ist bereit für ein Abenteuer. Bist du es auch?!\n\n {ut.char_to_text(char, name=False)}",
            parse_mode='HTML'
        )
        return ConversationHandler.END
    logger.warn('unhandled callback in cm_end')
    return END  # in case nothing happend stay in state


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  simple handler functions
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def error(bot, update, error):
    logger.exception('Update "%s" caused error "%s"' % (update, error))


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


def activate_char(bot, update, args):
    """ debug command, to manually select a character by id.
    """
    char = Character.objects.get(pk=args[0])
    player = ut.get_p_user(update.message.from_user)
    player.active_char = char
    player.save()
    update.message.reply_text(f'Charakter {char.name} aktiviert')


def callback(bot, update):
    """ this function is called when a button is pressed.
    The button data is a csv string, that is split and evaluated from left to
    right.
    """
    data = update.callback_query.data.split(',')
    msg = update.callback_query.message  # only works for normal bot msgs
    imsg_id = update.callback_query.inline_message_id # inline message ids
    logger.warn('callback update from msg %s', msg)
    player = ut.get_p_user(update.callback_query.from_user)

    # probe buttons
    if data[0] == 'probe':
        #char = Character.objects.get(pk=data[1])
        char = player.active_char
        if char is None:
            update.callback_query.answer(
                    text='Kein aktiver Charakter! Schreib mir privat.',
                    show_alert=True)
            return
        action = Action.objects.get(pk=data[2])
        malus = int(data[3])
        result = ut.probe(char, action, malus)
        em = '❌' if result < 0 else '✅'
        text = f'{em} {char.name} {action.name}: {result}'
        bot.edit_message_text(text=text, inline_message_id=imsg_id,
                            reply_markup=None)
        return

    # probe keyboard
    elif data[0] == 'extendprobekbd':
        logger.warn('probe keyboard extend')
        #msg_text = msg.text
        msg_kbd = msg.reply_markup
        btns = msg_kbd.inline_keyboard
        if len(btns) > 1: # collapse
            log('collapse probe keyboard')
            msg_kbd = InlineKeyboardMarkup([btns[0]])
        else:
            log('expand probe keyboard')
            roll_btn = btns[0][0]
            # get probe details from first button
            cb_data = roll_btn.callback_data.split(',')
            row_plus = []
            row_minus = []
            for i in range(1,5):
                cb_data[3] = str(i)
                row_plus.append(InlineKeyboardButton(
                        '{:+d}'.format(i), callback_data=','.join(cb_data)))
                cb_data[3] = str(-i)
                row_minus.append(InlineKeyboardButton(
                        '{:+d}'.format(-i), callback_data=','.join(cb_data)))
            btns.append(row_plus)
            btns.append(row_minus)
            msg_kbd(btns)
        # msg.edit_text(msg.text, reply_markup=msg_kbd)  # not woking with imsg
        bot.edit_message_reply_markup(msg_kbd)





def inlinequery(bot, update):
    """ handles the user input after @botname. Searches available char actions
    and turns them into a message with a roll-dice button.
    Since we need to store the message anyways I added a keyboard property to
    the InlineMessage model which will be created from the models json data,
    when `models.InlineMessage.keyboard` is accessed.
    # NOTE: imsg_id cannot be used as pk, because its not known before the
    message is actually postet, and asa its posted, msg reference is gone.
    # NOTE: 2) creating the message obj, before posting the message, leads to
    one object for each suggestion for every typed character.. that would mess
    up the db too fast. So no way around passing button data and create the obj
    on first click.. after than the obj id can be attached to the buttons cbd.
    # NOTE: 3) changed inlinefeedback settings, could one pass the info into
    the InlineQueryResultArticle.id??????? This is really hackish, but could be
    a solution in combination with feedback updates, which contain this id.
    """
    query = update.inline_query.query
    logger.warn('query update')
    p_user = ut.get_p_user(update.inline_query.from_user)
    char_id = ut.get_users_active_char_id(p_user)
    options = []  # collection of buttons with predefined answers
    actions = Action.objects.filter(name__startswith=query)
    # TODO: use chars actions instead of all
    for act in actions:
        btns = [[InlineKeyboardButton('🎲',
                    callback_data=f'probe,{char_id},{act.id},0'),
                InlineKeyboardButton('🎚',
                    callback_data='extendprobekbd')]]
        options.append(
            InlineQueryResultArticle(
                title=act.name,
                description=f'{act.name} Probe',
                id=uuid4(),
                input_message_content = InputTextMessageContent(f'{act.name}:'),
                reply_markup=InlineKeyboardMarkup(btns)
            ))
    update.inline_query.answer(options, cache_time=0)


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
    dp.add_handler(CommandHandler('normaltest', sharetest))
    dp.add_handler(CommandHandler('activate', activate_char, pass_args=True))
    # special handlers
    cm_handler = ConversationHandler(
        entry_points=[CommandHandler('cm', character_menu)],
        states={
            CHOOSE_ADDON: [CallbackQueryHandler(cm_choose_addon)],
            CREATE_CHARACTER: [CallbackQueryHandler(cm_name)],
            # CHARACTER_NAME: [CallbackQueryHandler(character_name)],
            BASICS: [MessageHandler(Filters.text, cm_stats_custom_name),CallbackQueryHandler(cm_stats)],
            # BASICS: [CallbackQueryHandler(cm_stats)],
            SPECIALS:[CallbackQueryHandler(cm_actions)],
            END: [CallbackQueryHandler(cm_end)]
        },
        fallbacks=[CommandHandler('cm', character_menu)]
    )
    dp.add_handler(cm_handler)
    dp.add_handler(CallbackQueryHandler(callback))
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_error_handler(error)


def main():
    """ function called by django-telegram-bot automatically on webhook
    """
    logger.warning('main function called')
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
    up.idle()
