from django.contrib import admin
from fsm_admin.mixins import FSMTransitionMixin

from base_station.races.models import (
    Race,
    RacePilot,
    Round,
    RoundEvent,
    RaceOptions,
    RaceType,
    RaceTemplate
)

class RoundInline(admin.StackedInline):
    model = Round
    readonly_fields = ('number', 'state', 'heat_number',)
    raw_id_fields = ('race',)
    extra = 0


class RacePilotInline(admin.StackedInline):
    model = RacePilot
    fields = ('heat_number', 'pilot', 'tracker',)
    readonly_fields = ('heat_number',)
    extra = 0


class RaceAdmin(admin.ModelAdmin):
    model = Race
    fields = ('name', 'event', 'current_round')
    inlines = (
        RoundInline,
        RacePilotInline
    )
    readonly_fields = ('created', 'modified',)
    raw_id_fields = ('event', 'current_round',)


class RoundAdmin(FSMTransitionMixin, admin.ModelAdmin):
    model = Round
    fieldsets = (
        ('', {
            'fields': ('state', 'number', 'created', 'modified')
        }),
        ('Race Details', {
            'fields': ('race',)
        }),
        ('Timing', {
            'fields': ('goal_start_time', 'goal_end_time', 'started_time', 'ended_time')
        })
    )
    list_display = ('number', 'heat_number', 'race', 'goal_start_time', 'state')
    search_fields = ('race',)
    date_heirachy = 'created'
    list_filter = ('state',)
    fsm_field = ['state',]
    readonly_fields = ('state', 'number', 'created', 'modified',)
    raw_id_fields = ('race',)


class RoundEventAdmin(admin.ModelAdmin):
    model = RoundEvent
    fieldsets = (
        ('', {
            'fields': ('round', 'tracker', 'trigger', 'created', 'modified')
        }),
    )
    list_display = ('round', 'tracker', 'trigger')
    search_fields = ('round',)
    list_filter = ('trigger',)
    readonly_fields = ('created', 'modified',)
    raw_id_fields = ('round', 'tracker')


admin.site.register(RaceOptions)
admin.site.register(RaceType)
admin.site.register(RaceTemplate)
admin.site.register(Race, RaceAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(RoundEvent, RoundEventAdmin)
