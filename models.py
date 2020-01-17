from django.db import models
from core.models import TelebotUser

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   telegram related models
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Projekt47User(models.Model):
    """ telegram user and its profile/settings for this bot.
    """
    telebot_user = models.OneToOneField(TelebotUser,
                        related_name='projekt47_user',
                        null=True, blank=True, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        try:
            return self.telebot_user.first_name
        except:
            return 'Anonym'


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   game related models
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Game(models.Model):
    """ Game is the combination of the base rules with addons.
    Example:
        name: PlanetPi
        text: Nachdem die Erde vollständig unbewohnbar wurde, und der Mars sich
            aufgrund alles zerstörender Stürme als schwieriger Wohnort
            herausgestellt hat. Bricht eine Gruppe mutiger Astronauten zu einem
            neu entdeckten Planeten `Pi` auf. Sie sind nicht die ersten dort.
        addons: [Basis, SciFi, PlanetPi]
    """
    name = models.CharField(max_length=200)
    text = models.TextField(null=True, blank=True)
    addons = models.ManyToManyField("Addon", related_name='games', null=True,
                                    blank=True)

    def __str__(self):
        return self.name


class Addon(models.Model):
    """ Set of rules, actions and stats
    Example:
      name: SciFi
      text: Enthält Werte und Aktionen die im Weltraum nützlich sein könnten.
            Kosmoskentniss, Navigation, Aliensprache
    """
    name = models.CharField(max_length=200)
    text = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Stat(models.Model):
    """ Character stat
    Example:
        abbr: Int
        name: Intelligenz
        text: Intelligenz hilft die richtigen Entscheidungen zu treffen.
        addon: SciFiPi
    """
    abbr = models.CharField(max_length=4)
    name = models.CharField(max_length=200)
    text = models.TextField(null=True, blank=True)
    addons = models.ManyToManyField(Addon, related_name='stats')

    def __str__(self):
        return '{} [{}]'.format(self.name,
                        ', '.join([a.name for a in self.addons.all()]))


class Action(models.Model):
    """ Any kind of action. To start the action probes vs all stats are rolled.
    if success the formula  is evaluated and the result is used to format the
    answer string like `result = answer.format(evaluate(formular))`. Multiple
    results are possible but number must match the placeholders in answer.
    """
    name = models.CharField(max_length=200)
    addons = models.ManyToManyField(Addon, related_name='actions')
    stats = models.ManyToManyField(Stat, related_name='actions',
                                null=True, blank=True)
    formula = models.CharField(max_length=200, null=True, blank=True) # '1*W+4'
    answer = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return '{} [{}]'.format(self.name,
                        ', '.join([a.name for a in self.addons.all()]))


class Character(models.Model):
    """ A players character, belongs to an addon and can have stats with values,
    and actions with values/level through relations.
    """
    owner = models.ForeignKey(Projekt47User, on_delete=models.CASCADE,
                                null=True, blank=True)
    name = models.CharField(max_length=200)
    game = models.ForeignKey(Game, related_name='characters',
                                on_delete=models.CASCADE)
    stats = models.ManyToManyField(Stat, through="CharStat")

    def __str__(self):
        return self.name


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
    char = models.ForeignKey(Character, on_delete=models.CASCADE)
    stat = models.ForeignKey(Stat, on_delete=models.CASCADE)
    value = models.FloatField(default=0)

    def __str__(self):
        return '{}: {} {}'.format(self.char.name, self.stat.name, self.value)
