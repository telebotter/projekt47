from core.models import TelebotUser
from projekt47.models import Projekt47User


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   db interaction
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def get_p_user(tg_user, update=False):
    """ check for existing telebot_user, get or create the respective
    projekt47 user (opt. update userdata i.e. names/language).
    """
    telebot_user, new = TelebotUser.objects.get_or_create(pk=tg_user.id)
    if update:
        telebot_user.first_name = tg_user.first_name
        telebot_user.last_name = tg_user.last_name
        telebot_user.username = tg_user.username
    if new or update:
        telebot_user.save()
    p_user, new = Projekt47User.objects.get_or_create(telebot_user=telebot_user)
    if new:
        p_user.save()
    return p_user
