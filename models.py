from django.db import models
from core.models import TelebotUser
import json
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


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
    owner = models.ForeignKey(Projekt47User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)


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
    text = models.TextField(null=True, blank=True)
    ressource = models.BooleanField(default=False)
    #addons = models.ManyToManyField(Addon, related_name='stats', blank=True)
    addon = models.ForeignKey(Addon, related_name='stats', blank=True, null=True, on_delete=models.SET_NULL)
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
    addon = models.ForeignKey(Addon, related_name='action', blank=True, null=True, on_delete=models.SET_NULL)
    stats = models.ManyToManyField(Stat, related_name='actions',
                                null=True, blank=True)
    formula = models.CharField(max_length=200, null=True, blank=True) # '1*W+4'
    answer = models.CharField(max_length=300, null=True, blank=True)
    special = models.BooleanField(default=False,
                                verbose_name='Skill nötig')

    def __str__(self):
        return '{} [{}]'.format(self.name, self.addon.name)


class Character(models.Model):
    """ A players character, belongs to an addon and can have stats with values,
    and actions with values/level through relations.
    """
    class Meta:
        verbose_name = 'Charakter'
        verbose_name_plural = 'Charaktere'
    owner = models.ForeignKey(Projekt47User, on_delete=models.SET_NULL,
                                null=True, blank=True)
    name = models.CharField(max_length=200)
    addon = models.ForeignKey(Addon, related_name='characters',
                                on_delete=models.CASCADE, null=True)
    stats = models.ManyToManyField(Stat, through="CharStat", limit_choices_to={'addon': addon})
    actions = models.ManyToManyField(Action, related_name='characters', related_query_name='characters', blank=True)  # only special actions
    skill_points = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


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
    addon = models.ForeignKey(Addon, related_name='meta_cards', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default='Meta Karte')
    short = models.CharField(max_length=400, default='Kurzbeschreibung der Metakarte (log, tooltip)') # log text and shord des
    text = models.CharField(max_length=500, default="Vollständige Erklärung der Metakarte")

    def __str__(self):
        return str(self.addon.name + ': ' + self.name)


class Names(models.Model):
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
