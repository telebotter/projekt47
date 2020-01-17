from django.db import models
from telebotter import TelebotUser

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
    games = models.ManyToManyField(Game, related_name='addons', null=True,
                                    blank=True)

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


class CharStat(models.Model):
    char = models.ForeignKey(Character, on_delete=models.CASCADE)
    stat = models.ForeignKey(Stat, on_delte=models.CASCADE)
    value = models.FloatField(default=0)

    def __str__(self):
        return '{}: {} {}'.format(self.char.name, self.stat.name, self.value)


class Action(models.Model):
    """ Any kind of action. To start the action probes vs all stats are rolled.
    if success the formula  is evaluated and the result is used to format the
    answer string like `result = answer.format(evaluate(formular))`. Multiple
    results are possible but number must match the placeholders in answer.
    """
    name = models.CharField(max_length=200)
    addons = models.ManyToMany(Addon, related_name='actions')
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
    owner = models.ForeignKey(Projekt47User, on_delte=models.CASCADE,
                                null=True, blank=True)
    name = models.CharField(max_length=200)
    game = models.ForeignKey(Game, related_name='characters',
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.name
