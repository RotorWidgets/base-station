from django.contrib import admin

from base_station.races.models import RaceHeat, HeatEvent


class RaceHeatAdmin(admin.ModelAdmin):
    model = RaceHeat
    fieldsets = (
        ('', {
            'fields': ('created', 'modified')
        }),
        ('Event Details', {
            'fields': ('event',)
        })
    )
    list_display = ('event', 'created')
    search_fields = ('event',)
    date_heirachy = 'created'
    # list_filter = ('event',)
    readonly_fields = ('created', 'modified',)


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


admin.site.register(RaceHeat, RaceHeatAdmin)
admin.site.register(HeatEvent, HeatEventAdmin)
