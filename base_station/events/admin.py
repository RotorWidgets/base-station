"""Admin views for the models of the ``events`` app."""
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from simple_history.admin import SimpleHistoryAdmin


from .models import (
    Event,
    EventTemplate,
    # EventCategory,
    Location,
    Occurrence,
)


# TODO: add SimpleHistoryAdmin and to model
class LocationAdmin(OSMGeoAdmin):
    fields = ('name', 'address', 'location', 'meta')
    list_display = ('name', 'address', 'location',)
    default_zoom = 8


class EventAdmin(SimpleHistoryAdmin):
    """Custom admin for the ``Event`` model."""
    model = Event
    fieldsets = (
        ('Occurence templates', {
            'fields': (
                ('title', 'title_template',),
                ('description', 'description_template')
            )
        }),
        ('Event Rules', {
            'fields': ('template',)
        }),
        ('Event times', {
            'fields': ('start', 'end', 'recurrences',)
        }),
        ('Event meta data', {
            'fields': ('location',)
            # 'category',
        })
    )
    list_display = (
        'title', 'start', 'end', )
        # 'category',
    search_fields = ('title', 'description',)
    date_hierarchy = 'start'
    # list_filter = ('category', )


# class EventCategoryAdmin(admin.ModelAdmin):
#     """Custom admin to display a small colored square."""
#     model = EventCategory
#     list_display = ('name',)
#     # list_editable = ('color',)


admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventTemplate, SimpleHistoryAdmin)
# admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(Occurrence)
