from django.contrib import admin

from projekt47.models import *

# Register your models here.
admin.site.register(Projekt47User)
admin.site.register(Adventure)
# admin.site.register(Stat)
# admin.site.register(Action)
# admin.site.register(CharStat)


# admin.site.register(Character)

class CharStatInline(admin.TabularInline):
    model = CharStat
    extra = 1


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    inlines = (CharStatInline,)


# define inline layouts to add them in other models admin form

class StatInline(admin.TabularInline):
    model = Stat
    extra = 1


class ActionInline(admin.TabularInline):
    model = Action
    extra = 1


class MetaCardInline(admin.TabularInline):
    model = MetaCard
    extra = 1


@admin.register(Addon)
class AddonAdmin(admin.ModelAdmin):
    inlines = [StatInline, ActionInline, MetaCardInline]
