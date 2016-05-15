import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from .races import Race
from base_station.pilots.models import Pilot
from base_station.trackers.models import Tracker
from base_station.utils.models import SyncModel


logger = logging.getLogger(__name__)


class RaceGroup(SyncModel, TimeStampedModel):
    """
    If a race is split up into different groups we store pilot relationships to this group
    """
    number = models.PositiveSmallIntegerField(
        _("Heat number"), blank=False, default=1)
    race = models.ForeignKey(Race, related_name='groups')
    pilots = models.ManyToManyField(Pilot, through='GroupPilot')

    class Meta:
        unique_together = ("number", "race")


class GroupPilot(SyncModel):
    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE)
    group = models.ForeignKey(RaceGroup, on_delete=models.CASCADE)

    # extra fields
    tracker = models.ForeignKey(Tracker, blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        # TODO: figure out a way to make pilots unique to the race.
        # Maybe store all pilots on the race and then have code that makes sure
        # There are no duplicates between race groups.
        unique_together = ("pilot", "group")
