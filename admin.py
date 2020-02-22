from django.contrib import admin
from django.urls import resolve
from projekt47.models import *

# Register your models here.
admin.site.register(Projekt47User)
admin.site.register(Adventure)
# admin.site.register(Stat)
# admin.site.register(Action)
# admin.site.register(CharStat)
admin.site.register(DefaultName)

import logging
logger = logging.getLogger(__name__)


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        self.instance = obj
        return super(ActionAdmin, self).get_form(request, obj=obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ["stat_1", "stat_2", "stat_3"]:
            kwargs["queryset"] = Stat.objects.filter(addon=self.instance.addon)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



# define inline layouts to add them in other models admin form

class CharStatInline(admin.TabularInline):
    model = CharStat
    extra = 1


class StatInline(admin.TabularInline):
    model = Stat
    extra = 1


class ActionInline(admin.TabularInline):
    model = Action
    extra = 1

    def get_parent_object_from_request(self, request):
        """
        Returns the parent object from the request or None.

        Note that this only works for Inlines, because the `parent_model`
        is not available in the regular admin.ModelAdmin as an attribute.
        """
        resolved = resolve(request.path_info)
        if resolved.kwargs:
            return self.parent_model.objects.get(pk=resolved.kwargs['object_id'])
        return None


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # is called but how to get addon instance?  prob use get_parent hack from here
        # https://stackoverflow.com/questions/14950193/how-to-get-the-current-model-instance-from-inlineadmin-in-django
        if db_field.name in ["stat_1", "stat_2", "stat_3"]:# and self.instance:
            addon = self.get_parent_object_from_request(request)
            kwargs["queryset"] = Stat.objects.filter(addon=addon)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class MetaCardInline(admin.TabularInline):
    model = MetaCard
    extra = 1

class ResInline(admin.TabularInline):
    model = Ressource
    extra = 1


@admin.register(Addon)
class AddonAdmin(admin.ModelAdmin):
    inlines = [StatInline, ResInline, ActionInline, MetaCardInline]

    def get_form(self, request, obj=None, **kwargs):
        self.instance = obj
        return super(AddonAdmin, self).get_form(request, obj=obj, **kwargs)


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    inlines = (CharStatInline,)
