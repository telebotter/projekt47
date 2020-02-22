from django.contrib import admin

from projekt47.models import *

# Register your models here.
admin.site.register(Projekt47User)
admin.site.register(Adventure)
# admin.site.register(Stat)
# admin.site.register(Action)
# admin.site.register(CharStat)
admin.site.register(DefaultName)



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
    form = ActionAdmin.form

    # def get_form(self, request, obj=None, **kwargs):
    #     self.instance = obj
    #     return super(ActionInline, self).get_form(request, obj=obj, **kwargs)
    #
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name in ["stat_1", "stat_2", "stat_3"] and hasattr(self, 'instance'):
    #         kwargs["queryset"] = Stat.objects.filter(addon=self.instance.addon)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)


class MetaCardInline(admin.TabularInline):
    model = MetaCard
    extra = 1

class ResInline(admin.TabularInline):
    model = Ressource
    extra = 1


@admin.register(Addon)
class AddonAdmin(admin.ModelAdmin):
    inlines = [StatInline, ResInline, ActionInline, MetaCardInline]

    # def get_form(self, request, obj=None, **kwargs):
    #     self.instance = obj
    #     return super(AddonAdmin, self).get_form(request, obj=obj, **kwargs)
    #
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name in ["stat_1", "stat_2", "stat_3"] and self.instance:  # and hasattr(self, 'instance'):
    #         kwargs["queryset"] = Stat.objects.filter(addon=self.instance.addon)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    inlines = (CharStatInline,)
