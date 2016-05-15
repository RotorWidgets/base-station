from datetime import datetime
import logging

from catalog import Catalog
from channels import Group
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from django_fsm import FSMIntegerField, transition

from base_station.events.models import Event
from base_station.pilots.models import Pilot
from base_station.trackers.models import Tracker
from base_station.utils.models import SyncModel


logger = logging.getLogger(__name__)


class Race(SyncModel, TimeStampedModel):
    """
    Container that is aware of what pilots are participating and their relevant trackers
    """

    name = models.CharField(_('Race Name'), max_length=100)
    event = models.ForeignKey(Event, related_name='races')
    # Relationship or property with state filter? probably relationship updated by state changes.
    # current_heat = models.ForeignKey('RaceHeat', blank=True, null=True)

    # TODO: scheduled times

    class Meta:
        unique_together = ("name", "event")

    def __str__(self):
        return "{}".format(self.name)


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
        # There are no duplicates within race groups.
        unique_together = ("pilot", "group")


class RaceHeatQuerySet(models.QuerySet):
    # For use in the future when we need to filter race heats by some mechanism
    pass


class RaceHeatState(Catalog):
    _attrs = 'value', 'label'
    waiting = 0, 'Waiting'
    running = 1, 'Running'
    restarting = 2, 'Restarting'
    ended = 3, 'Ended'


class RaceHeat(SyncModel, TimeStampedModel):
    """
    A heat represents a singular race in which multiple pilots are participating,
    A heat holds state that follows the designated race logic from the event.
    Race heats are auto generated for a given race from the settings
    and log the different times they start and stop.
    """

    number = models.PositiveSmallIntegerField(
        _("Heat number"), blank=False, default=1)
    race = models.ForeignKey(Race, related_name='heats')
    group = models.ForeignKey(RaceGroup, blank=True, null=True)
    state = FSMIntegerField(
        choices=RaceHeatState._zip("value", "label"),
        default=RaceHeatState.waiting.value)

    # created when the
    goal_start_time = models.DateTimeField(_("Heat goal start time"), blank=False)
    goal_end_time = models.DateTimeField(_("Heat goal end time"), blank=False)

    started_time = models.DateTimeField(_("Heat started time"), blank=True, null=True)
    ended_time = models.DateTimeField(_("Heat ended time"), blank=True, null=True)

    objects = RaceHeatQuerySet.as_manager()

    class Meta:
        unique_together = ("number", "race")

    def __str__(self):
        return "{!s} heat {!s}".format(self.race, self.number)

    @transition(
        field=state,
        source=[
            RaceHeatState.waiting.value,
            RaceHeatState.restarting.value,
        ],
        target=RaceHeatState.running.value)
    def start(self):
        # TODO: fails if there is already another heat running.
        self.started_time = datetime.now()
        self.ended_time = None

    @transition(
        field=state,
        source=RaceHeatState.running.value,
        target=RaceHeatState.ended.value
    )
    def end(self):
        self.ended_time = datetime.now()

    @transition(
        field=state,
        source=[
            RaceHeatState.running.value,
            RaceHeatState.ended.value,
        ],
        target=RaceHeatState.restarting.value)
    def restart(self):
        """
        Allow a finished or running race to be restarted.
        """
        self.started_time = None
        self.ended_time = None

    @property
    def started(self):
        # TODO: may tie this into the state machine
        return bool(self.started_time)

    @property
    def ended(self):
        return bool(self.ended_time)

    @property
    def event_template(self):
        return self.race.event.template

    @property
    def group_name(self):
        """Group name for use with channels"""
        return "{!s}-heat-{!s}".format(self.race.id, self.number)

    def get_channel_group(self):
        return Group(self.group_name)


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
    trigger = models.PositiveSmallIntegerField(
        _("trigger"), choices=TRIGGERS._zip("value", "label"))

    objects = HeatEventQuerySet.as_manager()

    def __str__(self):
        return "{!s} {!s}".format(self.tracker, self.get_trigger_display())
