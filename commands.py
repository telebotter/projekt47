import logging
import datetime as dt
from projekt47 import utils as ut
from projekt47.constants import *
from projekt47.models import *
from projekt47.models import Projekt47User
from django.conf import settings
from telebotter.utils import typing_action
import operator

logger = logging.getLogger(__name__)
commands = []


@typing_action
def add_sp(update, context):
    """ provides the active character of player one or more (args) SP.
    Works with negative numbers as well.
    """
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
commands.append(add_sp)


@typing_action
def activate_char(update, context):
    """ debug command, to manually select a character by id.
    """
    char = Character.objects.get(pk=args[0])
    player = ut.get_p_user(update.message.from_user)
    player.active_char = char
    player.save()
    update.message.reply_text(f'Charakter {char.name} aktiviert')
activate_char.text = 'Aktiviert einen Charakter ueber seine ID'
activate_char.aliases = ['aktiviere', 'aktivieren', 'activate', 'enable']
commands.append(activate_char)


@typing_action
def info_text(update, context):
    """ posts info text (story/description) of this users active char.
    TODO: ut.get_third_user() check message for mention entities or quoted
    message authors, to get those users activated char info instead.
    """
    tg_user = ut.get_third_user(update)
    player = ut.get_player(tg_user)
    char = player.active_char
    # check for image and send if it's there
    if char.image:
        # logger.warning(f'ImgField.url: {char.image.url}')
        update.message.reply_photo(photo=settings.BASE_URL+char.image.url,
                    quote=False, caption=char.info_text(), parse_mode='HTML')
    else:
        update.message.reply_text(char.info_text(), parse_mode='HTML', quote=False)
info_text.text = 'Infotext zu deinem Char oder dem eines Freundes (@/quote)'
info_text.aliases = ['info', 'infotext']
commands.append(info_text)


@typing_action
def info_stats(update, context):
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


@typing_action
def set_story(update, context):
    """ posted story vom aktuellen char wenn kein argument, ansonsten wird sie
    neu geschrieben.
    """
    player = ut.get_player(update.message.from_user)
    char = player.active_char
    if not len(context.args)>0:
        update.message.reply_text(f'Beschreibung: {char.text}')
        return
    story = ' '.join(context.args)
    char.text = story
    char.save()
    update.message.reply_text('Beschreibung geaendert!')
set_story.text = 'Schreibe einen kurzen Text zu deinem Charakter'
set_story.aliases = ['story', 'text', 'beschreibung']
commands.append(set_story)


@typing_action
def show_rules(update, context):
    """ posted alle regeln in kurz oder die nummer aus args in lang.
    """
    # handle arguments
    if len(context.args) > 0:
        try:
            text = RULES[int(context.args[0])-1]['long']
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
commands.append(show_rules)


@typing_action
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
draw_metacard.text = 'Ziehe eine Metakarte'
draw_metacard.aliases = ['metakarte', 'dc', 'draw', 'drawcard', 'meta', 'karte']
commands.append(draw_metacard)


@typing_action
def shit(update, context):
    """ draw a first meta card, or a new one with arg=neu
    """
    text = '💩'
    update.message.reply_text(text, parse_mode='HTML')
    return
shit.text = 'Kacke'
shit.aliases = ['shit']
commands.append(shit)


@typing_action
def ressource(update, context):
    """ shows current ressources of own char. if args add arg1 points to arg0.
    Example: `/res lp -5`
    """
    args = context.args
    bot = context.bot
    # tg_user = ut.get_user_or_quoted(update)
    tg_user = ut.get_third_user(update)
    player = ut.get_p_user(tg_user)
    char = player.active_char
    # no args just overview
    if len(args)<2:
        res_text = ''  # lines with chars ressources
        for cres in char.charres_set.all():
            res_text += f'<b>{cres.res.abbr}</b> {cres.res.name}: '
            res_text += f'{cres.current}/{cres.max}\n'
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
    text = MSG['resschange'].format(
            char.name, cres.res.name, cres_old, cres.current)
    update.message.reply_text(text)
    logger.info(text)
ressource.text = 'Zeigt oder aendert die aktuellen Ressourcen eines Spielers.'
ressource.aliases = ['res', 'vorraete', 'status', 'vitalitaet', 'ressourcen']
commands.append(ressource)


@typing_action
def test_probe(update, context):
    """ runs Action.probe for action taken from args. If args is int its taken
    as id, otherwise titles are searched for the arg and probe is run on all.
    """
    args = context.args
    player = ut.get_player(update.message.from_user)
    char = player.active_char
    if char is None:
        update.message.reply_text('Kein aktivierten char gefunden')

    if len(args) == 0:
        update.message.reply_text('Bitte gib mir ne ID oder ein Suchbegriff')
        return
    try:
        id = int(args[0])
        actions = [Action.objects.get(pk=id)]
    except ValueError:
        logger.debug('args are not int, use as search string')
        q = ' '.join(args)
        actions = Action.objects.filter(addon=char.addon, name__icontains=q)
    logger.info(f'found actions for query {q}: {len(actions)}')
    for a in actions:
        res = a.probe(char)
        update.message.reply_text(text=MSG['testprobe'].format(**res))
        logger.info(f'got result for test probe: {res}')
test_probe.text = 'WIP funktion zum testen verschiedener proben'
test_probe.aliases = ['testprobe', 'tp']
commands.append(test_probe)


@typing_action
def mega_test_probe(update, context):
    """ runs Action probe 1000 times and returns percentage and hists
    """
    args = context.args
    bot = context.bot
    try:
        import pandas as pd
        import datetime as dt
        from io import BytesIO
        import matplotlib.pyplot as plt
    except Exception:
        update.message.reply_text('library fehlt auf dem server')
        return
    player = ut.get_player(update.message.from_user)
    char = player.active_char
    if char is None:
        update.message.reply_text('Kein aktivierten char gefunden')

    if len(args) == 0:
        update.message.reply_text('Bitte gib mir ne ID oder ein Suchbegriff')
        return
    try:
        id = int(args[0])
        actions = [Action.objects.get(pk=id)]
    except ValueError:
        logger.debug('args are not int, use as search string')
        q = ' '.join(args)
        actions = Action.objects.filter(addon=char.addon, name__icontains=q)
    logger.info(f'found actions for query {q}: {len(actions)}')
    ress = {}
    a = actions[0] # only one for now
    #ress[a.name] =
    t_0 = dt.datetime.now()
    ress = {'diff': [], 'all': [], 'each': [],
            'diff_neach': [], 'diff_each': []}
    for i in range(1000):
        res = a.probe(char)
        ress['all'].append(int(res['all']))
        ress['each'].append(int(res['each']))
        ress['diff'].append(int(res['diff']))
        if res['each']:
            ress['diff_each'].append(int(res['diff']))
            ress['diff_neach'].append(0)
        else:
            ress['diff_neach'].append(int(res['diff']))
            ress['diff_each'].append(0)
    t = dt.datetime.now()-t_0
    logger.info(f'1000 pobes run in {t}')
    data = pd.DataFrame.from_dict(ress)
    plt.figure()
    ax = data['diff'].hist(bins=range(-10,10))
    ax.set_title(f'Probendifferenz: {a.name}')
    #plt.hist([data['diff_each'],data['diff_neach']], stacked=True, color = ['r','g'])
    iomage = BytesIO()
    iomage.name = 'histo.png'
    #plt.savefig(iomage)
    ax.figure.savefig(iomage)
    iomage.seek(0)
    mres = {
        'action': a.name,
        'each_p': sum(ress['each'])/10,
        'all_p': sum(ress['all'])/10,
        't': t.total_seconds(),
        'n': res['n'],
    }
    #update.message.reply_text(MSG['megaprobe'].format(**mres))
    bot.send_photo(update.message.chat_id, photo=iomage, caption=MSG['megaprobe'].format(**mres))
mega_test_probe.text = 'WIP funktion zum testen verschiedener proben'
mega_test_probe.aliases = ['megatestprobe', 'megatp', 'mtp']
commands.append(mega_test_probe)


@typing_action
def roll(update, context):
    """ rollt args wuerfel und gibt die einzel werte sowie die summe zurueck.
    """
    args = context.args
    try:
        n = int(args[0])
    except Exception:
        n = 1
    rolls = [rd.randint(1,6) for _ in range(n)]
    txt = '+'.join([ EMOJ_NUM[r] for r in rolls ])
    if len(rolls) > 1:
        txt += f' = {sum(rolls)}'
    update.message.reply_text(txt, parse_mode='HTML')
roll.text = 'Mehrfach würfeln'
roll.aliases = ['wuerfeln', 'wurf', 'roll']
commands.append(roll)


@typing_action
def triroll(update, context):
    """ shortcut fuer /roll 3 """
    context.args = ['3']
    roll(update, context)
triroll.text = 'Kurzform für /wuerfeln 3'
triroll.aliases = ['probe', 'triroll', 'dummyprobe']
commands.append(triroll)
