from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import InlineQueryResultArticle
from telegram import ParseMode
from telegram import InputTextMessageContent
from core.models import TelebotUser
from projekt47.models import Projekt47User
from projekt47.models import Action
from projekt47.models import Stat
from projekt47.constants import *
import random as rd
from uuid import uuid4
import logging
logger = logging.getLogger()



def log(msg):
    """ shortcut for simple logging """
    logger.info(msg)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   db interaction
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def get_p_user(tg_user, update=False):
    logger.warning('get_p_user() deprecated: renamed to get_player()')
    return get_player(tg_user, update=update)


def get_player(tg_user, update=False):
    """ check for existing telebot_user, get or create the respective
    projekt47 user (opt. update userdata i.e. names/language).
    """

    telebot_user, new = TelebotUser.objects.get_or_create(pk=tg_user.id)
    if new or update:
        telebot_user.first_name = tg_user.first_name
        telebot_user.last_name = tg_user.last_name
        telebot_user.username = tg_user.username
        telebot_user.save()
    p_user, new = Projekt47User.objects.get_or_create(telebot_user=telebot_user)
    if new:
        p_user.save()
    return p_user


def get_users_active_char_id(user):
    """ returns active char (id) of the user (projekt47user or tg user obj) or
    """
    if isinstance(user, Projekt47User):
        p_user = user
    else:  # expect a tg user or obj with similar parameters
        p_user = get_p_user(user)
    return p_user.active_char


def reset_charstats(user):
    return


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   game logic
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def roll(n=1):
    """ roll n dices and return their sum
    """
    rolls = [rd.randint(1,6) for _ in range(n)]
    logger.info(f'rolled: {rolls}')
    return sum(rolls)


def probe(char, action, malus=0):
    """ can also take a stat instead of an action
    returns probe_diff, diceresults, cstats_sum, number of dices
    """
    if isinstance(action, Stat):
        act_stats = [action]
    else:
        act_stats = action.stats.all()
    cstats = char.charstat_set.filter(stat__in=act_stats)
    logger.info(f'Character stats: {cstats}')
    cstats_sum = sum([s.value+malus for s in cstats])
    logger.info(f'csum {cstats_sum}')
    num_dice = cstats.count()
    res = roll(num_dice)
    probe_diff = res - cstats_sum
    logger.info(f'result: {probe_diff}')
    return probe_diff , res , cstats_sum , num_dice



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   telegram stuff
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def get_third_user(update):
    """ checks an update for quote and returns the quoted author. If not return
    author of message.
    # TODO: also check for entities and parse them (@mentions)?
    """
    if update.message.reply_to_message:
        return update.message.reply_to_message.from_user
    return update.message.from_user


def add_footer(keyboard, back, finish, cb='cm'):
    """ return list of button(s) or None, pass cb to use other callback prefix.
    """
    footer = []
    if back:
        footer.append(InlineKeyboardButton(BTN['back'],
                        callback_data='cm,back'))
    if finish:
        footer.append(InlineKeyboardButton(BTN['next'],
                        callback_data='cm,finish'))
    if len(footer) > 0:
        keyboard.append(footer)


def skill_keyboard(char, finish_btn=True, back_btn=True):
    """ return keybaord with available charstats an skill buttons with required
    callback data to identify and change them.
    """
    keyboard = []
    for cstat in char.charstat_set.filter(stat__ressource=False):
        stat = cstat.stat  # cstat contains the skill of the char, stat the meta
        keyboard.append([
            InlineKeyboardButton('-', callback_data=f'cm,skill,{cstat.id},-1'),
            InlineKeyboardButton(f'{EMOJ_NUM[cstat.value]} {cstat.stat.abbr}',
                                callback_data=f'cm,statalert,{cstat.stat.id}'),
            InlineKeyboardButton('+', callback_data=f'cm,skill,{cstat.id},+1'),
            ]
        )
    add_footer(keyboard, back_btn, finish_btn)
    return keyboard


def action_keyboard(char, finish_btn=True, back_btn=True):
    """ return keyboard with actions, a char can learn. Callback data is
    cm,skillaction,<action_id>.
    """
    keyboard = []
    logger.warn('action kbd')
    actions = Action.objects.filter(
            special=True, addon=char.addon)
    logger.warn(actions.count())
    actions = actions.exclude(characters__in=[char])
    logger.warn(actions.count())
    for action in actions:
        keyboard.append([InlineKeyboardButton(action.name,
                        callback_data=f'cm,skillaction,{action.id}')])
    add_footer(keyboard, back_btn, finish_btn)
    return keyboard


def probe_message(char, act):
    """ generates the message content for a probe. Can be used to generate
    message content for inlinequery results and regenerate the message when
    keyboard is extended (probe mali). It also returns the description for
    inline query results.
    """
    if isinstance(act, Stat):
        cbd = f'statprobe,{char.id},{act.id},'
        stats = [act]
        desc = act.abbr
    else:
        cbd = f'probe,{char.id},{act.id},'
        stats = act.stats.all()
    cstats = char.charstat_set.filter(stat__in=stats)
    n = len(stats)
    p = sum([c.value for c in cstats])
    desc = ', '.join([s.abbr for s in stats])
    msg_text = MSG['probe'].format(emoji='🎲', name=char.name,
             cstat_sum = str(p), action=act.name, wmoji = '❔', diff='❔', roll_sum='❔')
    btns = [[InlineKeyboardButton('🎲',
                callback_data=cbd+'0'),
            InlineKeyboardButton('📶',
                callback_data=cbd+'ext')]]
    return (msg_text, btns, desc)


def probe_query_result(char, act):
    """ generates the inline query result article (title, text and message) for
    a specific action of a character. Works also for stats instead of actions.
    """
    msg_text, btns, desc = probe_message(char, act)
    content = InputTextMessageContent(msg_text, parse_mode='HTML')
    res = InlineQueryResultArticle(
        title=act.name,
        description=desc,
        id=uuid4(),
        input_message_content = content,
        reply_markup=InlineKeyboardMarkup(btns))
    return res
