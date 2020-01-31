from core.models import TelebotUser
from projekt47.models import Projekt47User
from projekt47.models import Action
import random as rd
import logging
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
logger = logging.getLogger()

# dont access them as string, an emoji can be more than one char!
EMO_NUM = ['0️⃣', '1️⃣', '2️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

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
    if finish_btn:
        keyboard.append([InlineKeyboardButton('Fertig',
                        callback_data='cm,finish')])
    return keyboard


def action_keyboard(char, finish_btn=True):
    """ return keyboard with actions, a char can learn.
    NOTE: The used method is neither elegant nor efficient.
    TODO: Rewrite db queries (i.e. characters_not_contain=char)
    ISSUES: #8
    """
    keyboard = []
    logger.warn('action kbd')
    actions = Action.objects.filter(
            special=True, addon=char.addon)
    logger.warn(actions.count())
    actions = actions.exclude(characters__in=[char])
    logger.warn(actions.count())

    # TODO: do this with db query
    # known_actions = char.actions.all()
    # filter all actions
    for action in actions:
        # if action in known_actions:
        #     continue
        # # filter out requirements not met
        # met = True
        # for s in action.stats.all():
        #     cstat = char.charstat_set.get(stat=s)
        #     if not cstat:
        #         logger.warn(f'{char.name} hat kein {s.name}')
        #         met = False
        #         break  # dont cehck other stats
        #     elif cstat.value > 4:
        #         logger.warn(f'{char.name} hat zu wenig {s.name}')
        #         met = False
        #         break
        # if not met:
        #     continue
        keyboard.append([InlineKeyboardButton(action.name,
                        callback_data=f'cm,skillaction,{action.id}')])
    if finish_btn:
        keyboard.append([InlineKeyboardButton('Fertig',
                        callback_data='cm,finish')])
    return keyboard


def char_to_text(char, name=True, html=True):
    """ creates an overview of the character as text, ready to be used in
    a message.
    """
    bold = '<b>{}</b>' if html else '{}'
    n = bold.format(char.name)
    text = n+'\n\n' if name else ''
    text += 'Eigenschaften:\n'
    for s in char.charstat_set.all():
        text += ' ' + EMO_NUM[s.value] + ' ' + s.stat.name + '\n'
    text += '\nSpezialaktionen:'
    for a in char.actions.all():
        text += f"\n *️⃣ {a.name}"
    return text
