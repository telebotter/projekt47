import logging
import datetime as dt
from projekt47 import utils as ut
from projekt47.constants import *
logger = logging.getLogger(__name__)


commands = []


def add_sp(bot, update, args):
    """ provides the active character of player one or more (args) SP.
    Works with negative numbers as well.
    """
    # check for linked user (entity)
    # NOTE: Mentions sind uncool, weil nur in gruppe moeglich und nervt
    # entities = update.message.parse_entities()
    # mentions = []
    # for entity in entities:
    #     logger.info(f'entety: {entity}')
    #     parsed_entity = update.message.parse_entity(entity)
    #     logger.info(f'parsed: {parsed_entity}')
    #     if entity['user']:
    #         logger.info(f'found user: {entity["user"]}')
    player = ut.get_p_user(update.message.from_user)
    char = player.active_char
    if not char:
        update.message.reply_text(MSG['nochar'])
    old_sp = char.skill_points
    try:
        delta = int(args[0])
    except Exception as e:
        logger.debug(e)
        delta = 1
    new_sp = old_sp + delta
    char.skill_points = new_sp
    char.save()
    msg = f'Skillpunkte von {char.name} angepasst: {old_sp} -> {new_sp}'
    update.message.reply_text(msg, quote=False)
add_sp.text = 'Gib deinem activen Charakter einen oder mehrere Skillpunkte.'
add_sp.aliases = ['addskillpoints', 'addskillpoint',
                'skillpunkt', 'skillpunkte', 'xp']
add_sp.args = True  # TODO: this should be obsolet when context is used.
commands.append(add_sp)


def info_text(bot, update, args):
    """ posts info text (story/description) of this users active char.
    TODO: ut.get_third_user() check message for mention entities or quoted
    message authors, to get those users activated char info instead.
    """
    player = ut.get_p_user(update.message.from_user)
    char = player.active_char
    update.message.reply_text(char.info_text(), parse_mode='HTML')
info_text.text = 'Infotext zu deinem Char oder dem eines Freundes (@/quote)'
info_text.aliases = ['info', 'infotext']
info_text.args = True
commands.append(info_text)


def info_stats(bot, update, args):
    """ posts stats text (story/description) of this users active char.
    TODO: ut.get_third_user() check message for mention entities or quoted
    message authors, to get those users activated char info instead.
    """
    player = ut.get_p_user(update.message.from_user)
    char = player.active_char
    update.message.reply_text(char.info_stats(), parse_mode='HTML')
info_stats.text = 'Statistik zu deinem Char oder dem eines Freundes (@/quote)'
info_stats.aliases = ['stats', 'werte', 'daten', 'statstext', 'charakter']
info_stats.args = True
commands.append(info_stats)


def set_story(bot, update, args):
    """ posted story vom aktuellen char wenn kein argument, ansonsten wird sie
    neu geschrieben.
    """
    player = ut.get_p_user(update.message.from_user)
    char = player.active_char
    if not len(args)>0:
        update.message.reply_text(f'Beschreibung: {char.text}')
        return
    story = ' '.join(args)
    char.text = story
    char.save()
    update.message.reply_text('Beschreibung geaendert!')
set_story.text = 'Schreibe einen kurzen Text zu deinem Charakter'
set_story.aliases = ['story', 'text', 'beschreibung']
set_story.args = True
commands.append(set_story)
