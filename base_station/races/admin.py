from django.contrib import admin
from fsm_admin.mixins import FSMTransitionMixin

from base_station.races.models import Race, RaceGroup, RaceHeat, HeatEvent


class RaceHeatInline(admin.StackedInline):
    model = RaceHeat
    extra = 0


class RaceGroupInline(admin.StackedInline):
    model = RaceGroup
    fields = ('number',)
    readonly_fields = ('number', )
    extra = 0


class RaceAdmin(admin.ModelAdmin):
    model = Race
    fields = ('name', 'event')
    inlines = (
        RaceHeatInline,
        RaceGroupInline
    )
    readonly_fields = ('created', 'modified',)


class RaceHeatAdmin(FSMTransitionMixin, admin.ModelAdmin):
    model = RaceHeat
    fieldsets = (
        ('', {
            'fields': ('state', 'number', 'created', 'modified')
        }),
        ('Timing', {
            'fields': ('goal_start_time', 'goal_end_time', 'started_time', 'ended_time')
        }),
        ('Race Details', {
            'fields': ('race',)
        })
    )
    list_display = ('group_name', 'race', 'created', 'state')
    search_fields = ('race',)
    date_heirachy = 'created'
    list_filter = ('state',)
    fsm_field = ['state',]
    readonly_fields = ('state', 'number', 'created', 'modified',)
    raw_id_fields = ('race',)


class HeatEventAdmin(admin.ModelAdmin):
    model = HeatEvent
    fieldsets = (
        ('', {
            'fields': ('heat', 'tracker', 'trigger', 'created', 'modified')
        }),
    )
    list_display = ('heat', 'tracker', 'trigger')
    search_fields = ('heat',)
    list_filter = ('trigger',)
    readonly_fields = ('created', 'modified',)
    raw_id_fields = ('heat', 'tracker')


admin.site.register(Race, RaceAdmin)
admin.site.register(RaceHeat, RaceHeatAdmin)
admin.site.register(HeatEvent, HeatEventAdmin)
