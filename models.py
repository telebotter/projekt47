from django.db import models
from core.models import TelebotUser
from projekt47.constants import *
import json
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from django.template.loader import render_to_string
import logging
import random as rd
logger = logging.getLogger(__name__)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   telegram related models
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class Projekt47User(models.Model):
    """ telegram user and its profile/settings for this bot.
    """
    class Meta:
        verbose_name = 'Spieler'
        verbose_name_plural = 'Spieler'
    telebot_user = models.OneToOneField(TelebotUser,
                        related_name='projekt47_user',
                        null=True, blank=True, on_delete=models.CASCADE)
    active_char = models.ForeignKey("Character", on_delete=models.SET_NULL,
                        null=True, blank=True)

    def __str__(self):
        try:
            return str(self.telebot_user.first_name)
        except:
            return 'Unbekannt'


# class InlineMessage(models.Model):
#     """ Represents a TelegramInlineMessage with collapsable keyboard. Used to
#     keep text and keyboard of probe messages (the one with the roll button).
#     """
#     imsg_id = models.BigIntegerField(null=True, blank=True)  # inline_message_id
#     collapsed = models.BooleanField(default=False)  # only first line shown
#     kbd_json = models.CharField()  # json string of button data
#     # [[{text: 'btn1', data: 'probe,1,2'}]]
#     text = models.CharField(max_length=600, null=True, blank=True)
#     from_user = models.ForeignKey(Projekt47User, null=True, blank=True)
#     date_created = models.DateTimeField(auto_now_add=True)  # TODO: autonow create
#     date_edit = models.DateTimeField(auto_now=True)  # TODO: auto now touch
#
#     def __str__(self):
#         return self.id
#
#     @property
#     def keyboard(self):
#         """ property returns (collapsed) TelegramInlineKeyboard from this obj
#         """
#         btns = []
#         for row in json.loads(self.kbd.json):
#             btns.append([ InlineKeyboardButton(btn['text'],
#                                 callback_data=btn['data'])
#                         for btn in row])
#             if self.collapsed:
#                 break  # stop adding further rows wenn kbd is collapsed
#         return InlineKeyboardMarkup(btns)



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   game related models
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class Addon(models.Model):
    """ Set of rules, actions and stats. Every Char has to belong to one addon.
    Example:
      name: SciFi
      text: Enthält Werte und Aktionen die im Weltraum nützlich sein könnten.
            Kosmoskentniss, Navigation, Aliensprache
    """
    class Meta:
        verbose_name = 'Addon'
        verbose_name_plural = 'Addons'
    name = models.CharField(max_length=200)
    text = models.TextField(null=True, blank=True)
    skill_points = models.IntegerField(default=3)
    owner = models.ForeignKey(Projekt47User,
            blank=True, null=True, on_delete=models.SET_NULL)
    # act_probe_fill = models.BooleanField(default=True,
    #         verbose_name='Vier Werte pro Aktion')
    # act_probe_sum = models.BooleanField(default=False,
    #         verbose_name='Werte in Aktionen summieren')

    def __str__(self):
        return str(self.name)

    def card_context(self):
        ctx =  {
            'title': self.name,
            'url': self.id,
            'footer': 'Autor: ' + str(self.owner),
        }
        return ctx


class Adventure(models.Model):
    """ One adventure or story, that belongs to a game and is told by the GM.
    """
    class Meta:  # namen in admin backend
        verbose_name = 'Abenteuer'
        verbose_name_plural = 'Abenteuer'
    name = models.CharField(max_length=150)
    addon = models.ForeignKey(Addon, on_delete=models.CASCADE, null=True)
    parent = models.ForeignKey("Adventure", null=True, blank=True,
                                        on_delete=models.SET_NULL)
    duration = models.FloatField(null=True, blank=True, verbose_name='Dauer')
    player_min = models.IntegerField(null=True, blank=True,
                                        verbose_name='Minimale Spielerzahl')
    player_max = models.IntegerField(null=True, blank=True,
                                        verbose_name='Maximale Spielerzahl')
    preview = models.CharField(max_length=1024, null=True, blank=True,
                                        verbose_name='Kurzbeschreibung')
    text = models.TextField(verbose_name='Text')

    def __str__(self):
        return str(self.name)


class Stat(models.Model):
    """ Character stat
    Example:
        abbr: In
        name: Intelligenz
        text: Intelligenz hilft die richtigen Entscheidungen zu treffen.
        addon: SciFiPi
    """
    class Meta:
        verbose_name = 'Wert'
        verbose_name_plural = 'Werte'
    abbr = models.CharField(max_length=4)
    name = models.CharField(max_length=200)
    text = models.CharField(max_length=180, null=True, blank=True)
    ressource = models.BooleanField(default=False)
    #addons = models.ManyToManyField(Addon, related_name='stats', blank=True)
    addon = models.ForeignKey(Addon, related_name='stats',
            blank=True, null=True, on_delete=models.SET_NULL)
    emoji = models.CharField(max_length=8, null=True, blank=True)

    def __str__(self):
        return '{} [{}]'.format(self.name, self.addon.name)


class Ressource(models.Model):
    """ Ressource is a stat that is has a fixed maximum and minimum and can be
    modified during the game. Like mana and health.
    """
    class Meta:
        verbose_name = 'Ressource'
        verbose_name_plural = 'Ressourcen'
    abbr = models.CharField(max_length=4)
    name = models.CharField(max_length=200)
    text = models.TextField(null=True, blank=True)
    addon = models.ForeignKey(Addon, related_name='ressources',
            blank=True, null=True, on_delete=models.SET_NULL)
    scale = models.IntegerField(default=10, verbose_name='Skillfaktor')
    emoji = models.CharField(max_length=8, null=True, blank=True)

    def __str__(self):
        return '{} [{}]'.format(self.name, self.addon.name)


class Action(models.Model):
    """ Any kind of action. To start the action probes vs all stats are rolled.
    if success the formula  is evaluated and the result is used to format the
    answer string like `result = answer.format(evaluate(formular))`. Multiple
    results are possible but number must match the placeholders in answer.
    """
    class Meta:
        verbose_name = 'Aktion'
        verbose_name_plural = 'Aktionen'
    name = models.CharField(max_length=200)
    addon = models.ForeignKey(Addon, related_name='actions',
            blank=True, null=True, on_delete=models.SET_NULL)
    stats = models.ManyToManyField(Stat, related_name='actions',
            null=True, blank=True)
    formula = models.CharField(max_length=200, null=True, blank=True) # '1*W+4'
    answer = models.CharField(max_length=300, null=True, blank=True)
    special = models.BooleanField(default=False,
            verbose_name='Skill nötig')
    stat_1 = models.ForeignKey(Stat, related_name='stats_1',
            blank=True, null=True, on_delete=models.SET_NULL)
    stat_2 = models.ForeignKey(Stat, related_name='stats_2',
            blank=True, null=True, on_delete=models.SET_NULL)
    stat_3 = models.ForeignKey(Stat, related_name='stats_3',
            blank=True, null=True, on_delete=models.SET_NULL)
    stat_4 = models.ForeignKey(Stat, related_name='stats_4',
            blank=True, null=True, on_delete=models.SET_NULL)

    @property
    def stat_list(self):
        return [stat_1, stat_2, stat_3, stat_4]

    def __str__(self):
        return '{} [{}]'.format(self.name, self.addon.name)

    def probe(self, char):
        """ rolls evaluates the action for a passed character and returns the
        result. Returns dict:
        'res_sum': true/false,
        'diff': summed probe diff,
        """
        stats = [self.stat_1, self.stat_2, self.stat_3, self.stat_4]
        cstats = []
        for s in stats:
            cs = char.charstat_set.filter(stat=s).first()
            if cs is not None:
                cstats.append(cs.value)
        # remove None values
        # cstats = [v for v in cstats if v is not None]
        cstasts = list(filter(None.__ne__, cstats))  # faster than list compr?
        n = len(cstats)
        logger.debug(f'found {n} character values {cstats} for: {self.name}')
        cstat_sum = sum(cstats)
        rolls = [rd.randint(1,6) for _ in range(n)]
        roll_sum = sum(rolls)
        each = True
        for i in range(n):
            if rolls[i] <= cstats[i]:
                each = False
                break
        all = (cstat_sum < roll_sum)
        result = {
            'action': self.name,
            'n': n,
            'each': each,
            'all': all,
            'cstats': cstats,
            'cstat_sum': cstat_sum,
            'rolls': rolls,
            'roll_sum': roll_sum,
            'diff': roll_sum - cstat_sum
        }
        return result




class Character(models.Model):
    """ A players character, belongs to an addon and can have stats with values,
    and actions with values/level through relations.
    """
    class Meta:
        verbose_name = 'Charakter'
        verbose_name_plural = 'Charaktere'
    owner = models.ForeignKey(Projekt47User,
            on_delete=models.SET_NULL,
            null=True, blank=True)
    name = models.CharField(max_length=200)
    addon = models.ForeignKey(Addon,
            related_name='characters',
            on_delete=models.CASCADE,
            null=True, blank=True)
    stats = models.ManyToManyField(Stat,
            through="CharStat",
            limit_choices_to={'addon': addon})
    ress = models.ManyToManyField(Ressource,
            through="CharRes",
            limit_choices_to={'addon': addon})
    actions = models.ManyToManyField(Action,
            related_name='characters',
            related_query_name='characters',
            null=True, blank=True)  # only special actions
    skill_points = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)
    text = models.TextField(null=True, blank=True)
    meta_card = models.ForeignKey('MetaCard',
            null=True, blank=True,
            verbose_name='Meta Karte',
            related_name='chars',
            on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)

    def info_text(self, html=True, name=True):
        """ returns a string with optional name/addon as header. It contains the
        characters description Char.text and can be used as message text.
        """
        b = '<b>{}</b>' if html else '{}'
        i = '<i>{}</i>' if html else '{}'
        header = b.format(self.name) + '\n'
        header += i.format(str(self.addon)) + '\n\n'
        text = header if name else ''
        text += str(self.text)
        if self.meta_card:
            text += '\n\n' + self.meta_card.msg(html=html)
        return text

    def info_stats(self, html=True, name=True):
        """ creates an overview of the characters stats as text, ready to be
        used in a message.
        """
        bold = '<b>{}</b>' if html else '{}'
        n = bold.format(self.name)
        text = n+'\n\n' if name else ''
        text += 'Eigenschaften:\n'
        for s in self.charstat_set.all():
            text += ' ' + EMOJ_NUM[s.value] + ' ' + s.stat.name + '\n'
        text += '\nSpezialaktionen:'
        for a in self.actions.all():
            text += f"\n *️⃣ {a.name}"
        return text


class Session(models.Model):
    """ An adventure is played in a session, the session stores story related
    details and settings. Players (Projekt47User) can join a session, with a
    character from a respective game. Owner of a session is the GM.
    """
    owner = models.ForeignKey(Projekt47User, on_delete=models.SET_NULL,
                                null=True, blank=True)
    name = models.CharField(max_length=200, default='unnamed')
    addon = models.ForeignKey(Addon, related_name='sessions',
                                on_delete=models.SET_NULL, null=True)
    characters = models.ManyToManyField(Character, related_name='sessions',
                                null=True, blank=True)

    def __str__(self):
        return '{} [{}]'.format(self.name, self.game.name)


class MetaCard(models.Model):
    """ bonus regeln zB trinken bei pasch etc.. um zusatz fun einzubauen
    greifen nicht in die bot logik ein ermöglichen dem spieler aber bestimmte
    andere handlungen.. die er/gm ausspielen muss..
    """
    class Meta:
        verbose_name = 'Metakarte'
        verbose_name_plural = 'Metakarten'
    addon = models.ForeignKey(Addon,
            related_name='meta_cards',
            on_delete=models.CASCADE)
    name = models.CharField(max_length=200,
            default='Meta Karte')
    short = models.CharField(max_length=400,
            default='Kurzbeschreibung der Metakarte (log, tooltip)')
    text = models.CharField(max_length=500,
            default="Vollständige Erklärung der Metakarte")
    impact = models.IntegerField(default=0, verbose_name='Spieleinfluss')
    face_down = models.BooleanField(default=False, verbose_name='verdeckt')

    def __str__(self):
        return str(self.addon.name + ': ' + self.name)

    def msg(self, html=True):
        b = '<b>{}</b>' if html else '{}'
        return b.format(self.name) + '\n' + self.text


class DefaultName(models.Model):
    """ Namens vorschlaege bei der generierung von characteren.
    """
    name = models.CharField(max_length=80, default='Noname')
    addon = models.ForeignKey(Addon,
        related_name='default_names',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    def __str__(self):
        return str(self.addon.name + ': ' + self.name)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   relations between classes
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class CharStat(models.Model):
    """ Relation between character and stat. Stats are unique, as there is only
    one object `strength` for example but multiple relations to this. Relations
    that need additional information become its own class, like this one.
    Documentation to this concept:
    https://docs.djangoproject.com/en/2.2/topics/db/models/#extra-fields-on-many-to-many-relationships
    To create such relations, with add/create shortcuts pass a through_default:
    ```
    >>> char.stats.add(mystat, through_defaults={'value': 10})
    >>> char.stats.create(name="Stärke", abbr="St" through_defaults={'value': 10})
    >>> char.stats.set([st, in, wi, ge], through_defaults={'value': 10)})
    ```
    TODO: does this work also in reverse?
    ```
    >>> stat.chars.add(mychar, through_defaults={'value': 10})
    >>> stat.chars.set([char1, char2], through_defaults={'value': 10)})
    ```
    """
    class Meta:
        verbose_name = 'Charakterwert'
        verbose_name_plural = 'Charakterwerte'
        constraints = [
            models.UniqueConstraint(fields=['char', 'stat'], name='uni_skill'),
        ]
    char = models.ForeignKey(Character, on_delete=models.CASCADE)
    stat = models.ForeignKey(Stat, on_delete=models.CASCADE)
    value = models.IntegerField(default=4)

    def __str__(self):
        return '{}: {} {:+d}'.format(self.char.name, self.stat.name, self.value)


class CharRes(models.Model):
    class Meta:
        verbose_name = 'Charakterressource'
        verbose_name_plural = 'Charakterressourcen'
        constraints = [
            models.UniqueConstraint(fields=['char', 'res'], name='uni_charres'),
        ]
    char = models.ForeignKey(Character, on_delete=models.CASCADE)
    res = models.ForeignKey(Ressource, on_delete=models.CASCADE)
    max = models.IntegerField(default=100)
    current = models.IntegerField(default=100)

    def __str__(self):
        return '{}: {} {:+d}'.format(self.char.name, self.res.name, self.max)


# class CharAction(models.Model):
#     """ character specific information of an action, like level/skill
#     not used yet.. chars either can use an ability or cant.. they scale with
#     stats no action skill.
#     """
#     char = models.ForeignKey(Character, on_delete=models.CASCADE)
#     act = models.ForeignKey(Action, on_delete=models.CASCADE)
#     value = models.IntegerField(default=0)
#
#     def __str__(self):
#         return '{}: {} {:+d}'.format(self.char.name, self.act.name, self.value)
