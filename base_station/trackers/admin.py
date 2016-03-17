from django.contrib import admin

from .models import Tracker


class TrackerAdmin(admin.ModelAdmin):
    model = Tracker
    fields = ('id', 'transponder_id', 'tracker_type')
    readonly_fields = ('id',)


admin.site.register(Tracker, TrackerAdmin)
