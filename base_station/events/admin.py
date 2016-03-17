from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Event, EventTemplate


admin.site.register(Event, SimpleHistoryAdmin)
admin.site.register(EventTemplate, SimpleHistoryAdmin)
