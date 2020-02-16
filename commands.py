import logging
import datetime as dt
from projekt47 import utils as ut
from projekt47.constants import *
from projekt47.models import *
from projekt47.models import Projekt47User
import operator

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
    tg_user = ut.get_third_user(update)
    player = ut.get_player(tg_user)
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
    tg_user = ut.get_third_user(update)
    player = ut.get_player(tg_user)
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
    tg_user = ut.get_third_user(update)
    player = ut.get_player(tg_user)
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
    player = ut.get_player(update.message.from_user)
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


def show_rules(bot, update, args):
    """ posted alle regeln in kurz oder die nummer aus args in lang.
    """
    # handle arguments
    if len(args) > 0:
        try:
            text = RULES[int(args[0])-1]['long']
            update.message.reply_text(text)
        except:
            update.message.reply_text(MSG['norule'])
        finally:
            return
    # no argument
    rules = [EMOJ_NUM[i+1] + ' ' + ru['short'] for i, ru in enumerate(RULES)]
    rule_text = '\n\n'.join(rules)
    text = MSG['rules'].format(URLS['rules'], rule_text)
    update.message.reply_text(text, parse_mode='HTML')
show_rules.text = 'Zeigt Regeln als Uebersicht oder im Volltext an'
show_rules.aliases = ['regeln', 'rules', 'regel', 'rule']
show_rules.args = True
commands.append(show_rules)


def draw_metacard(bot, update, args):
    """ draw a first meta card, or a new one with arg=neu
    """
    player = ut.get_player(update.message.from_user)
    char = player.active_char
    if not char.meta_card or 'neu' in args:
        card = MetaCard.objects.filter(addon=char.addon).order_by('?').first()
        char.meta_card = card
        char.save()
        logger.info(f'{char} zieht Metakarte: {card.name}')
        update.message.reply_text(card.msg(), parse_mode='HTML')
        return
    text = char.meta_card.msg() + '\n\n' + MSG['hasmetacard']
    update.message.reply_text(text, parse_mode='HTML')
draw_metacard.text = 'Ziehe eine Metakarte.'
draw_metacard.aliases = ['metakarte', 'dc', 'draw', 'drawcard', 'meta', 'karte']
draw_metacard.args = True
commands.append(draw_metacard)


def ressource(bot, update, args):
    """ shows current ressources of own char. if args add arg1 points to arg0.
    Example: `/res lp -5`
    """
    # tg_user = ut.get_user_or_quoted(update)
    tg_user = ut.get_third_user(update)
    player = ut.get_p_user(tg_user)
    char = player.active_char
    # no args just overview
    if len(args)<2:
        res_text = ''  # lines with chars ressources
        for cres in char.charres_set.all():
            res_text += f'<b>{cres.res.abbr}</b> {cres.res.name}: {cres.current}/{cres.max}\n'
        msg_text = MSG['ress'].format(char.name, res_text)
        update.message.reply_text(msg_text, parse_mode='HTML')
        return
    # with at least to args:
    # use get instead of filter and first or just filter (list). This should
    # always return one cres if not there should be an error raised.
    # if cres.count() < 1:
    #     log.warning("No ressource found for {args[0]}")
    #     update.message.reply_text(MSG['nores'].format(args[0]))
    #     return
    # elif cres.count() > 1:
    #     log.error(f"To many char ress found for {args[0]}")
    #     log.info(str(update))
    #     update.message.reply_text(MSG['error'])
    #     return
    # __iexact makes comparism case insensitive
    try:
        cres = char.charres_set.get(res__abbr__iexact=args[0])
    except ValueError as ve:
        logging.error(ve)
        update.message.reply_text('Konnte die Zahl nicht erahnen.')
        return
    except Exception as e:
        logging.error(e)
        update.message.reply_text(MSG['error'])
        return
    cres_old = cres.current
    # set new value and clamp it to (0,res.max)
    cres.current = max(min(cres.current+int(args[1]), cres.max), 0)
    cres.save()
    text = MSG['resschange'].format(char.name, cres.res.name, cres_old, cres.current)
    update.message.reply_text(text)
    logger.info(text)
ressource.text = 'Zeigt oder aendert die aktuellen Ressourcen eines Spielers.'
ressource.aliases = ['res', 'vorraete', 'status', 'vitalitaet', 'ressourcen']
ressource.args = True
commands.append(ressource)
