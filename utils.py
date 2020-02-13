from core.models import TelebotUser
from projekt47.models import Projekt47User
from projekt47.models import Action
import random as rd
import logging
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
logger = logging.getLogger()

# dont access them as string, an emoji can be more than one char!
EMO_NUM = ['0️⃣', '1️⃣', '2️⃣','3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

def log(msg):
    """ shortcut for simple logging """
    logger.info(msg)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   db interaction
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def get_p_user(tg_user, update=False):
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
    TODO: raise GameError: NoCharSelected
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
    logger.warn(f'rolled: {rolls}')
    return sum(rolls)


def probe(char, action, malus=0):
    """ returns sum(dice) - sum(char.stat+malus)
    """
    act_stats = action.stats.all()
    cstats = char.charstat_set.filter(stat__in=act_stats)
    logger.warn(f'Character stats: {cstats}')
    cstats_sum = sum([s.value+malus for s in cstats])  # TODO: as query?
    logger.warn(f'csum {cstats_sum}')
    res = roll(cstats.count()) - cstats_sum
    logger.warn(f'result: {res}')
    return res


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   messages and strings
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def skill_keyboard(char, finish_btn=True):
    """ return keybaord with available charstats and skill buttons with required
    callback data to identify and change them.
    """
    keyboard = []
    for cstat in char.charstat_set.filter(stat__ressource=False):
        stat = cstat.stat  # cstat contains the skill of the char, stat the meta
        keyboard.append([
            InlineKeyboardButton('-', callback_data=f'cm,skill,{cstat.id},-1'),
            InlineKeyboardButton(f'{EMO_NUM[cstat.value]} {cstat.stat.abbr}',
                                callback_data=f'cm,statalert,{cstat.stat.id}'),
            InlineKeyboardButton('+', callback_data=f'cm,skill,{cstat.id},+1'),
            ]
        )
    footer = []
    if finish_btn:
        footer.append([InlineKeyboardButton('Fertig',
                        callback_data='cm,finish')])
    if back_btn:
        footer.append([InlineKeyboardButton('🔙',
                        callback_data='cm,back')])
    if len(footer)>0:
        keyboard.append(footer)
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
    footer = []
    if finish_btn:
        footer.append([InlineKeyboardButton('Fertig',
                        callback_data='cm,finish')])
    if back_btn:
        footer.append([InlineKeyboardButton('🔙',
                        callback_data='cm,back')])
    if len(footer)>0:
        keyboard.append(footer)
    return keyboard
