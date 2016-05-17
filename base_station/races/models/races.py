import logging

from channels import Group
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
# from django_fsm import FSMIntegerField, transition

from base_station.events.models import Event
from base_station.pilots.models import Pilot
from base_station.trackers.models import Tracker
from base_station.utils.models import SyncModel
# from .templates import RaceTemplate


logger = logging.getLogger(__name__)


class Race(SyncModel, TimeStampedModel):
    """
    Container that is aware of what pilots are participating and their relevant trackers
    """

    name = models.CharField(_('Race Name'), max_length=100)
    event = models.ForeignKey(Event, related_name='races')
    current_round = models.OneToOneField(
        'Round', blank=True, null=True, related_name='current_of')
    pilots = models.ManyToManyField(Pilot, through='RacePilot')
    # template = models.ForeignKey(RaceTemplate)

    # TODO: scheduled times

    class Meta:
        unique_together = ("name", "event")

    def __str__(self):
        return "{}".format(self.name)

    # TODO: mechanism for adding pilots and having them auto assigned to a group.

    @property
    def group_name(self):
        """Group name for use with channels"""
        return "race-{!s}".format(self.race.pk)

    def get_channel_group(self):
        return Group(self.group_name)

    def add_pilot(self, pilot, request=None):
        logger.info('Adding {!s} pilot to race {!s}'.format(pilot, self))
        self.pilots.add(pilot)


class RacePilot(SyncModel):
    heat_number = models.PositiveSmallIntegerField(
        _("Heat"), blank=False, default=1)
    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)

    # extra fields
    tracker = models.ForeignKey(Tracker, blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    # added_by = User that added this pilot to the race if applicable

    class Meta:
        unique_together = ("pilot", "race")
