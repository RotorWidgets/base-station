from catalog import Catalog
from django.db import models
from django_extensions.db.models import TimeStampedModel

from base_station.events.models import Event
from base_station.trackers.models import Tracker
from base_station.utils.models import UUIDModel


# class Race(UUIDModel, TimeStampedModel):
#     """
#     Container that is aware of what trackers are participating
#     """
#     pass
#

# class RaceGroup(UUIDModel, TimeStampedModel):
#     """
#
#     """


class RaceHeat(UUIDModel, TimeStampedModel):
    """
    A heat represents a singular race in which multiple racers are participating,
    A heat had state that follows the designated race logic from the event.
    """

    event = models.ForeignKey(Event)

    # May get this relationship from the event relationship?
    @property
    def event_template(self):
        return self.event.template

    def __str__(self):
        return "{} heat".format(self.event)


class EVENT_TRIGGERS(Catalog):
    _attrs = ('value', 'label', 'serializer_label')
    gate = (0, 'Gate Trigger', 'gate')
    area_enter = (1, 'Area Entered Trigger', 'enter')
    area_exit = (2, 'Area Exit Trigger', 'exit')
    crash = (3, 'Crash Trigger', 'crash')
    land = (4, 'Land Trigger', 'land')
    takeoff = (5, 'Takeoff Trigger', 'takeoff')
    arm = (6, 'Arm Trigger', 'arm')
    disarm = (7, 'Disarm Trigger', 'disarm')


class HeatEventQuerySet(models.QuerySet):

    def tracker_events(self):
        return self.filter(tracker__isnull=False)

    def non_tracker_events(self):
        return self.filter(tracker__isnull=True)

    def for_tracker(self, tracker):
        return self.filter(tracker=tracker)


class HeatEvent(UUIDModel, TimeStampedModel):
    """
    Holds information about a race event and details about how it was triggered.
    """
    # heat this event belongs to
    heat = models.ForeignKey(RaceHeat, related_name='events')
    # tracker that triggered the event if available
    tracker = models.ForeignKey(Tracker, related_name='events', blank=True, null=True)
    trigger = models.PositiveSmallIntegerField(
        choices=EVENT_TRIGGERS._zip('value', 'label'))

    objects = HeatEventQuerySet.as_manager()

    def __str__(self):
        return "{!s} {!s}".format(self.tracker, self.get_trigger_display())
