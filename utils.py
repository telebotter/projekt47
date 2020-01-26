from core.models import TelebotUser
from projekt47.models import Projekt47User
import random as rd
import logging
logger = logging.getLogger()


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


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   game logic
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def roll(n=1):
    """ roll n dices and return their sum
    """
    rolls = [random.randint(1,6) for _ in range(n)]
    log(f'rolled: {rolls}')
    return sum(rolls)


def probe(char, action, malus=0):
    """ returns sum(dice) - sum(char.stat+malus)
    """
    cstats = char.charstats_set.filter(stat__in=action.stats)
    log(f'Character stats: {cstats}')
    cstats_sum = sum([s.value+malus for s in cstats])  # TODO: as query?
    log(f'csum {cstat_sum}')
    res = roll(cstats.count()) - cstats_sum
    log(f'result: {res}')
    return res
