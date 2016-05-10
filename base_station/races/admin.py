from django.contrib import admin

from base_station.races.models import Race, RaceGroup, RaceHeat, HeatEvent


class RaceHeatInline(admin.StackedInline):
    model = RaceHeat


class RaceGroupInline(admin.StackedInline):
    model = RaceGroup
    fields = ('number',)
    readonly_fields = ('number', )


class RaceAdmin(admin.ModelAdmin):
    model = Race
    fields = ('name', 'event')
    inlines = (
        RaceHeatInline,
        RaceGroupInline
    )


class RaceHeatAdmin(admin.ModelAdmin):
    model = RaceHeat
    fieldsets = (
        ('', {
            'fields': ('number', 'created', 'active', 'modified')
        }),
        ('Timing', {
            'fields': ('goal_start_time', 'goal_end_time', 'started_time', 'ended_time')
        }),
        ('Race Details', {
            'fields': ('race',)
        })
    )
    list_display = ('group_name', 'race', 'created')
    search_fields = ('race',)
    date_heirachy = 'created'
    list_filter = ('active',)
    readonly_fields = ('number', 'created', 'modified',)


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


admin.site.register(Race, RaceAdmin)
admin.site.register(RaceHeat, RaceHeatAdmin)
admin.site.register(HeatEvent, HeatEventAdmin)
