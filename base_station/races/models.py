import logging
import json

from catalog import Catalog
from channels import Group
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from base_station.events.models import Event
from base_station.trackers.models import Tracker
from base_station.utils.models import SyncModel


logger = logging.getLogger(__name__)

# class Race(SyncModel, TimeStampedModel):
#     """
#     Container that is aware of what trackers are participating
#     """
#     pass
#

# class RaceGroup(SyncModel, TimeStampedModel):
#     """
#
#     """

class RaceHeatQuerySet(models.QuerySet):
    # For use in the future when we need to filter race heats by some mechanism
    pass


class RaceHeat(SyncModel, TimeStampedModel):
    """
    A heat represents a singular race in which multiple racers are participating,
    A heat holds state that follows the designated race logic from the event.
    """

    number = models.PositiveSmallIntegerField(
        _("Heat number"), blank=False, default=1)
    event = models.ForeignKey(Event)

    started_time = models.DateTimeField(_("Heat started time"), blank=True, null=True)
    ended_time = models.DateTimeField(_("Heat ended time"), blank=True, null=True)

    objects = RaceHeatQuerySet.as_manager()

    class Meta:
        unique_together = ("number", "event")

    @property
    def started(self):
        return bool(self.started_time)

    @property
    def ended(self):
        return bool(self.ended_time)

    @property
    def event_template(self):
        return self.event.template

    @property
    def group_name(self):
        return "heat-{!s}".format(self.number)

    def __str__(self):
        return "{} heat".format(self.event)


class HeatEventQuerySet(models.QuerySet):

    def tracker_events(self):
        return self.filter(tracker__isnull=False)

    def non_tracker_events(self):
        return self.filter(tracker__isnull=True)

    def for_tracker(self, tracker):
        return self.filter(tracker=tracker)


class HeatEvent(SyncModel, TimeStampedModel):
    """
    Holds information about a heat event and details about how it was triggered.
    """

    class TRIGGERS(Catalog):
        _attrs = ("value", "label", "serializer_label")
        gate = (0, _("Gate Trigger"), "gate")
        area_enter = (1, _("Area Entered Trigger"), "enter")
        area_exit = (2, _("Area Exit Trigger"), "exit")
        crash = (3, _("Crash Trigger"), "crash")
        land = (4, _("Land Trigger"), "land")
        takeoff = (5, _("Takeoff Trigger"), "takeoff")
        arm = (6, _("Arm Trigger"), "arm")
        disarm = (7, _("Disarm Trigger"), "disarm")
        started = (8, _("Start Trigger"), "started")
        ended = (9, _("End Trigger"), "ended")

    # heat this event belongs to
    heat = models.ForeignKey(RaceHeat, related_name="triggered_events")
    # tracker that triggered the event if available
    tracker = models.ForeignKey(Tracker, related_name="triggered_events", blank=True, null=True)
    # TODO: make a Category choice field?
    trigger = models.PositiveSmallIntegerField(
        _("trigger"), choices=TRIGGERS._zip("value", "label"))

    objects = HeatEventQuerySet.as_manager()

    def __str__(self):
        return "{!s} {!s}".format(self.tracker, self.get_trigger_display())
