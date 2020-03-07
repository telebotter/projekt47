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
from telegram.error import BadRequest  # for example edit message not changed
from django.conf import settings
from django_telegrambot.apps import DjangoTelegramBot  # for webmode
from projekt47 import utils as ut
from projekt47.commands import commands
from projekt47.models import *
from projekt47.constants import *
from uuid import uuid4
import random
import logging
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
import os
import io
# import pwd
#
# # Run when import
logger = logging.getLogger(__name__)
# os_user = pwd.getpwuid(os.getuid()).pw_name
# logger.debug(f'loading projekt47 module by user: {os_user}')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  character creation / conversation frame
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #



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
    player = ut.get_player(update.message.from_user)
    chars = Character.objects.filter(owner=player)
    for char in chars:
        btn = f'{char.name}'
        if char == player.active_char:
            btn = f'✔️ {char.name.upper()}'
        keyboard.append([
                InlineKeyboardButton(btn,
                        callback_data=f'cm_select,{char.id}')])
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
    logger.debug(f'select/create char')
    query = update.callback_query
    data = query.data.split(',')
    player = ut.get_player(query.from_user)

    # select existing
    if data[0] == 'cm_select':
        logger.info(f'{player} is selecting a char')
        char = Character.objects.get(pk=data[1])
        text = MSG['charselected'].format(char.name)
        btns = [
            [InlineKeyboardButton('Aktivieren',
                    callback_data=f'cm_activate,{char.id}')],
            [InlineKeyboardButton('Bearbeiten',
                    callback_data=f'cm_edit,{char.id}')],
            [InlineKeyboardButton('Loeschen',
                    callback_data=f'cm_delete,{char.id}')],
        ]
        query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(btns))
        return STUPIDNUMBER

    # init new character
    logger.info(f'{player} is creating a new char')
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


def cm_selected(bot, update):
    """ this is called when a player has chosen some operation on an existing
    character.
    """
    query = update.callback_query
    player = ut.get_player(query.from_user)
    data = query.data.split(',')
    char = Character.objects.get(pk=data[1])
    if data[0] == 'cm_activate':
        player.active_char = char
        player.save()
        query.edit_message_text(f'Dein Charakter {char.name} ist nun aktiv.',
                reply_markup=None)
        logger.info(f'{player} activated {char.name}')
        return ConversationHandler.END
    elif data[0] == 'cm_edit':
        player.active_char = char
        player.save()
        # quick jump to skill bypass conversationhandler steps
        # return SPECIALS
        return cm_stats(bot, update)
    elif data[0] == 'cm_delete':
        logger.info(f'{player} delete char {char.name}')
        char.delete()
        query.edit_message_text(f'Dein Charakter wurde geloescht.',
                reply_markup=None)
        return ConversationHandler.END


def cm_name(bot, update):
    """ Saves previous choice (addon).
    Send some suggestions for names or read from user input.
    """
    query = update.callback_query
    player = ut.get_player(query.from_user)
    char = player.active_char

    # set players stats and actions and save addon choice
    addon_id = int(query.data.split(',')[1])
    addon = Addon.objects.get(pk=addon_id)
    char.addon = addon
    char.skill_points = addon.skill_points
    for stat in addon.stats.all():
        char.stats.add(stat, through_defaults={'value': 4})
    for res in addon.ressources.all():
        char.ress.add(res, through_defaults={'current': 100})
    char.save()

    # next message
    text = MSG['askname']
    default_names = DefaultName.objects.filter(addon=addon).order_by('?')[:4]
    keyboard = [[InlineKeyboardButton(n.name,
            callback_data=f'cm,name,{n.name}')]
                for n in default_names]
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
                    callback_data=f'cm,name,{update.message.text}')]])
    update.message.reply_text(text, reply_markup=reply_markup)


def cm_stats(bot, update):
    """Saves previous choice (name).
    Gather all stats that are available for the selected addon and list them.
    The function has to be called everytime one of the stats change.
    #TODO: track unset stats (freie Skillpunkte).
    """
    query = update.callback_query
    player = ut.get_player(query.from_user)
    data = query.data.split(',')
    # save choice name
    if data[1] == 'name':
        name = data[2]
        player.active_char.name = name
        player.active_char.save()
    # next message
    text = MSG['skillgrade'].format(player.active_char.skill_points)
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
    player = ut.get_player(query.from_user)
    char = player.active_char
    data = query.data.split(',')

    # if button not from character manu, log and return
    if not data[0] == 'cm':  # ignore unrelated callbacks
        logger.warning(f'unhandled button pressed in skill view: {data}')
        return SPECIALS

    # user pressed the stat button
    elif data[1] == 'statalert':
        # user pressed the stat name, open description popup and stay in state
        stat = Stat.objects.get(pk=data[2])
        query.answer(text=f'{stat.name} ({stat.abbr}): {stat.text}',
                        show_alert=True)
        return SPECIALS

    # user pressed +1 or -1 (data[3]) for a stat (data[2])
    elif data[1] == 'skill':
        delta = int(data[3])  # button data +1 or -1
        stat_id = int(data[2])  # which stat should be changed
        # check free SP available
        new_sp = char.skill_points + delta
        if new_sp < 0:
            # return without saving or updating anything
            query.answer(MSG['nospleft'])
            return SPECIALS
        # check stat limits (>0, <6)
        cstat = CharStat.objects.get(pk=data[2])
        logger.info(f'Old Stat: {cstat.value}')
        new_stat = cstat.value + delta
        logger.info(f'New Stat: {new_stat}')
        if new_stat < 1 or new_stat > 6:
            # return without saving or updating anything
            query.answer('Nur Werte von 1-6 erlaubt!')
            return SPECIALS
        # remove actions that are not longer allowed
        if new_stat > 4:
            rem_acts = char.actions.filter(stats__in=[cstat.stat])
            rem_count = rem_acts.count()
            if rem_acts.count() > 0:
                logger.error('removed actions')
                query.answer(MSG['nostatreq'])
                new_sp += rem_count
                logger.error(f'sp added: {rem_acts.count()}')
                for a in rem_acts:
                    char.actions.remove(a)
                    logger.info(f'removed {a}')


        # change values in db
        char.skill_points = new_sp
        char.save()
        logger.info(f'{player} free SP changed ({delta}): {new_sp}')
        cstat.value = new_stat
        cstat.save()
        logger.info(f'{player} skilled ({delta}): {cstat}')
        # update message view:
        char.refresh_from_db()  # cb stats and actions changed
        markup = InlineKeyboardMarkup(ut.skill_keyboard(char))
        try:
            bot.edit_message_text(chat_id=query.message.chat_id,
                                message_id=query.message.message_id,
                                text=MSG['skill'].format(char.skill_points),
                                reply_markup=markup)
        except BadRequest as e:
            logger.debug(e)
            query.answer("Keine Aenderung festgestellt!")
        return SPECIALS  # stay in skill state

    # user finished skill (stats) go to skill actions
    elif data[1] == 'finish':
        # TODO: is active_char updated from db or already cached?
        # To be sure remove probably rerferenced character:
        player.refresh_from_db(fields=['active_char'])
        keyboard = ut.action_keyboard(player.active_char)
        reply_markup= InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=(  f"Skille deinen Character.\n"
                    f"Verbleibende Punkte: {char.skill_points}"),
            reply_markup=reply_markup
        )
        return END
    elif data[1] == 'back':
        query.answer('Sorry den Namen kannst du nichtmehr aendern!')
        return SPECIALS # dont go back to name

    # every button should be processed:
    logger.error('cbdata does not match anything: {data}')
    return SPECIALS


def cm_end(bot, update):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over
    TODO: loop the action skill keyboard until finish is pressed
    """
    query = update.callback_query
    data = query.data.split(',')
    player = ut.get_player(query.from_user)
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
        text = (f"Skille deinen Character.\n"
                f"Verbleibende Punkte: {char.skill_points}")
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
            text=(f"<b>{char.name}</b> ist bereit für ein Abenteuer.\n"
                f"Bist du es auch?!\n\n {char.info_stats(name=False)}"),
            parse_mode='HTML'
        )
        return ConversationHandler.END
    elif data[1] == 'back':
        text = MSG['statsagain'].format(char.skill_points)
        reply_markup = InlineKeyboardMarkup(ut.skill_keyboard(char))
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=text,
            reply_markup=reply_markup
        )
        return SPECIALS
    logger.warning('unhandled callback in cm_end')
    return END  # in case nothing happend stay in state


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  simple handler functions
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def error(bot, update, error):
    logger.exception(f'PTB Handled Error (update in bot log): {error}')
    logger.info(f'update that caused an error: {str(update)}')


def start(bot, update):
    tg_user = update.message.from_user
    p_user = ut.get_player(tg_user, update=True)
    update.message.reply_text(f'hallo {p_user.telebot_user.first_name}')


def devtest(bot, update):
    update.message.reply_text('Ich bin der pollende test bot')


def webtest(bot, update):
    update.message.reply_text('Ich bin der offizielle web bot')


def sharetest(bot, update):
    update.message.reply_text('Ich bin eine normale antwort')


def callback(bot, update):
    """ this function is called when a button is pressed.
    The button data is a csv string, that is split and evaluated from left to
    right.
    """
    query = update.callback_query
    data = query.data.split(',')
    msg = query.message  # only works for normal bot msgs
    imsg_id = query.inline_message_id # inline message ids
    logger.debug('callback update from msg %s', msg)
    player = ut.get_player(update.callback_query.from_user)
    char = player.active_char

    # cm data should not reach this handler:
    if data[0] == 'cm':
        logger.warning(f'{player} pressed cm button without conversation')
        query.answer('Buttons nichtmehr aktuell.')
        return

    # probe buttons
    if data[0].endswith('probe'):
        logger.info(data)
        if char is None:
            update.callback_query.answer(
                    text=MSG['nochar'],
                    show_alert=True)
            return
        if data[0] == 'probe':
            action = Action.objects.get(pk=data[2])
        # pass a stat as fake action
        elif data[0] == 'statprobe':
            act_stat = Stat.objects.get(pk=data[2])
            action = act_stat.as_action()
        else:
            logger.error('unexpected cbd for probe')
            return
        if data[3] == 'ext':
            logger.info('probe keyboard extend')
            # text, kbd, desc = ut.probe_message(char, action, ext=True)
            # msg.edit_text(msg.text, reply_markup=msg_kbd)  # not woking with imsg
            cbd = ','.join(data[:3])
            logger.info(f'cbd: {cbd}')
            rows = [[
                InlineKeyboardButton('🎲', callback_data=cbd+',0'),
                InlineKeyboardButton('👁‍🗨', callback_data=cbd+',0,hidden')]
            ]
            mali = [[-4, -3, -2, -1], [1, 2, 3, 4]]
            for r in mali:
                row = []
                for m in r:
                    data[3] = str(m)
                    cbd = ','.join(data)
                    btn = InlineKeyboardButton(f'{m:+d}', callback_data=cbd)
                    row.append(btn)
                rows.append(row)
            query.edit_message_reply_markup(InlineKeyboardMarkup(rows))
            return
        malus = int(data[3])
        # probe_diff , res , cstats_sum , num_dic = action.probe(char, action, malus)
        result = action.probe(char, malus=malus) #, malus)
        result['name'] = char.name
        if all([i == 1 for i in result['rolls']]):
            emoji = '💩💩💩'
            update.message.reply_text('💩', parse_mode='HTML')
        elif all([i == 6 for i in result['rolls']]):
            emoji = '🏆🏆🏆'
            update.message.reply_text('🥳', parse_mode='HTML')
        elif all([i <= 2 for i in result['rolls']]):
            emoji = '💩'
        elif all([i >= 5 for i in result['rolls']]):
            emoji = '🏆'
        elif result['diff'] <= 0:
            emoji = '❌'
        else:
            emoji = '✅'
        result['emoji'] = emoji
        wmojis = ''.join([ str(EMOJ_NUM[i]) for i in result['rolls'] ])
        result['wmoji'] = wmojis
        text = MSG['probe'].format(**result)
        if len(data) > 4 and data[4] == 'hidden':
            logger.info('hidden probe')
            text = MSG['probehidden'].format(**result)
            query.answer(text, show_alert=True)
            query.edit_message_reply_markup(None)
            return
        query.edit_message_text(text=text,
                reply_markup=None, parse_mode='HTML')
        return


    # xp collection
    elif data[0] == 'xpbox':
        # TODO: this has to be in conversation handler (possible for groups?)
        # TODO: to make sure old messages cannot be clicked any longer or click
        # TODO: state has to be saved in context/db.. VALIDATION NEEDED
        char = player.active_char
        if char is None:
            update.callback_query.answer(
                    text='Kein aktiver Charakter! Schreib mir privat.',
                    show_alert=True)
            return
        logger.warning(f'{player} versucht Skillpunkte einzusammeln.')
        if data[1] == 'single':
            xp = int(data[2])
            char.skill_points += xp
            char.save()
            text = f'{char.name} hat {xp} Erfahrungspunkte erhalten.'
            bot.edit_message_text(text=text, inline_message_id=imsg_id,
                                reply_markup=None)
            return
        if data[1] == 'group':
            query.answer('Fuer Gruppenloot fehlt noch ein konkreter Ansatz.')
            return


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
    logger.debug('query update')
    player = ut.get_player(update.inline_query.from_user)
    char = player.active_char
    char_id = ut.get_users_active_char_id(player)
    # https://docs.djangoproject.com/en/dev/topics/db/queries/#complex-lookups-with-q-objects
    actions = Action.objects.filter(
            (Q(special=False) | Q(characters__in=[char])),
            name__icontains=query,
            addon=char.addon)
    stats = Stat.objects.filter(addon=char.addon, name__icontains=query)
    logger.info(f'found stats for query: {stats.count()}')
    act_opts = [ut.probe_query_result(char, act) for act in actions]
    stat_opts = [ut.probe_query_result(char, stat) for stat in stats]
    options = act_opts + stat_opts
    # XP only when typed in...  TODO: GM tool/info
    if query.startswith('xp'):
        try:
            xp = int(query.split('xp')[-1])
        except ValueError:
            xp = 1
        options.append(
            InlineQueryResultArticle(
                title='Spieler XP',
                description=f'{xp} Skillpunkte vergeben',
                id=uuid4(),
                input_message_content = InputTextMessageContent(
                        'Erfahrungspunkte fuer einen Spieler.'),
                reply_markup=InlineKeyboardMarkup([
                                [InlineKeyboardButton('nehmen',
                                    callback_data=f'xpbox,single,{xp}')]])
            ))
        options.append(
            InlineQueryResultArticle(
                title='Gruppen XP',
                description=f'{xp} Skillpunkte an alle vergeben',
                id=uuid4(),
                input_message_content = InputTextMessageContent(
                        'Erfahrungspunkte fuer alle Spieler.'),
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                        'nehmen', callback_data=f'xpbox,group,{xp}')]])
            ))
    update.inline_query.answer(options, cache_time=0)


def handle_image(bot, update):
    player = ut.get_player(update.message.from_user)
    char = player.active_char
    if char is None:
        logger.warning('image from user without active char')
        return
    logger.info('setting new image')
    for p in update.message.photo:
        logger.info(f'width: {p.width}')
    photo = update.message.photo[-1]
    #image_stream = io.BytesIO()
    #photo.get_file().download(out=image_stream)
    tg_file = photo.get_file()
    fname = os.path.join('projekt47/avatars/', str(uuid4()) + '.jpg')
    fpath = os.path.join(settings.MEDIA_ROOT, fname)
    tg_file.download(custom_path=fpath)
    char.image.name = fname
    char.save()
    #logger.info(type(image))

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
    dp.add_handler(MessageHandler(Filters.document.image, handle_image))
    dp.add_handler(MessageHandler(Filters.photo, handle_image))

    # add handlers for commands.py
    for cmd in commands:
        pass_args = getattr(cmd, 'args', False)  # will be obsolete with context
        for alias in cmd.aliases:
            logger.info(f'adding {alias}')
            dp.add_handler(CommandHandler(alias, cmd, pass_args=pass_args))

    # special handlers
    cm_handler = ConversationHandler(
        entry_points=[CommandHandler('cm', character_menu)],
        states={
            CHOOSE_ADDON: [CallbackQueryHandler(cm_choose_addon)],
            CREATE_CHARACTER: [CallbackQueryHandler(cm_name)],
            # CHARACTER_NAME: [CallbackQueryHandler(character_name)],
            BASICS: [MessageHandler(Filters.text, cm_stats_custom_name),
                        CallbackQueryHandler(cm_stats)],
            # BASICS: [CallbackQueryHandler(cm_stats)],
            SPECIALS:[CallbackQueryHandler(cm_actions)],
            END: [CallbackQueryHandler(cm_end)],
            STUPIDNUMBER:[CallbackQueryHandler(cm_selected)],
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
    logger.debug('main function called')
    # dp = DjangoTelegramBot.getDispatcher('telebotterbot')
    dp = DjangoTelegramBot.getDispatcher(settings.PROJEKT47_BOT)
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
