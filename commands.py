import logging
import datetime as dt
from projekt47 import utils as ut
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
        update.message.reply_text('Du hast keinen Charakter aktiviert.')
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
add_sp.text = 'Gibt deinem activen Charakter einen oder mehrere Skillpunkte.'
add_sp.aliases = ['addskillpoints', 'addskillpoint',
                'skillpunkt', 'skillpunkte', 'xp']
add_sp.args = True  # TODO: this should be obsolet when context is used.
commands.append(add_sp)
