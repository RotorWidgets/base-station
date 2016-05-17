from datetime import datetime
import logging

from catalog import Catalog
from channels import Group
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from django_fsm import FSMIntegerField, transition

from base_station.trackers.models import Tracker
from base_station.utils.models import SyncModel
from .races import Race, RacePilot


logger = logging.getLogger(__name__)


class RoundQuerySet(models.QuerySet):

    def race_pilots(self):
        """All pilots participating in this round"""
        return RacePilot.objects.filter(race=self.race, heat_number=self.heat_number)


class RoundState(Catalog):
    _attrs = 'value', 'label'
    waiting = 0, 'Waiting'
    running = 1, 'Running'
    restarting = 2, 'Restarting'
    ended = 3, 'Ended'


class Round(SyncModel, TimeStampedModel):
    # TODO-FIX: I may be confusing rounds and rounds. Where rounds are incremented, and rounds are the groups.
    """
    A round represents a singular race in which multiple pilots are participating,
    A round holds state that follows the designated race logic from the event.
    Race rounds are auto generated for a given race from the settings
    and log the different times they start and stop.
    """

    number = models.PositiveSmallIntegerField(_("Round"), blank=False, default=1)
    race = models.ForeignKey(Race, related_name='rounds')
    heat_number = models.PositiveSmallIntegerField(_("Heat"), blank=False, default=1)
    state = FSMIntegerField(
        choices=RoundState._zip("value", "label"),
        default=RoundState.waiting.value)

    # created when the
    goal_start_time = models.DateTimeField(_("Round goal start time"), blank=False)
    goal_end_time = models.DateTimeField(_("Round goal end time"), blank=False)

    started_time = models.DateTimeField(_("Round started time"), blank=True, null=True)
    ended_time = models.DateTimeField(_("Round ended time"), blank=True, null=True)

    objects = RoundQuerySet.as_manager()

    ACTIVE_STATES = (RoundState.running.value, RoundState.restarting.value)

    class Meta:
        unique_together = (
            ("number", "race"),
            ("number", "heat_number")
        )
        ordering = ('number',)

    def __str__(self):
        return "{!s} round {!s}".format(self.race, self.number)

    def save(self, *args, **kwargs):
        if self._state.adding:
            # When adding a new round increment the round number automatically
            max_query = self.race.rounds.filter(
                heat_number=self.heat_number).aggregate(models.Max('number'))
            max_number = max_query['number__max'] or 0
            self.number = max_number + 1
        # wat, not sure what
        self.get_channel_group().send({'saved': True})
        super().save(*args, **kwargs)

    def start_condition(self):
        """Checks that there are no active rounds, excludes current round"""
        return not bool(
            self.race.rounds.filter(state__in=self.ACTIVE_STATES).exclude(pk=self.pk))

    @transition(
        field=state,
        source=[
            RoundState.waiting.value,
            RoundState.restarting.value,
        ],
        target=RoundState.running.value,
        conditions=[start_condition])
    def start(self):
        """Allow a waiting or restarted round to be started"""
        self.race.current_round = self
        self.race.save()
        self.started_time = datetime.now()
        self.ended_time = None

    @transition(
        field=state,
        source=RoundState.running.value,
        target=RoundState.ended.value)
    def end(self):
        """Allow a running round to be ended"""
        self.ended_time = datetime.now()

    @transition(
        field=state,
        source=[
            RoundState.running.value,
            RoundState.ended.value,
        ],
        target=RoundState.restarting.value)
    def restart(self):
        """Allow a finished or running race round to be restarted."""
        # Currently you can restart a round with another in an active state,
        # do may need to restrict it to when nothing is active?
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
        return "{!s}-round-{!s}".format(self.race.id, self.number)

    def get_channel_group(self):
        return Group(self.group_name)


class RoundEventQuerySet(models.QuerySet):

    def tracker_events(self):
        return self.filter(tracker__isnull=False)

    def non_tracker_events(self):
        return self.filter(tracker__isnull=True)

    def for_tracker(self, tracker):
        return self.filter(tracker=tracker)


class RoundEvent(SyncModel, TimeStampedModel):
    """
    Holds information about a round event and details about how it was triggered.
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

    # round this event belongs to
    round = models.ForeignKey(Round, related_name="triggered_events")
    # tracker that triggered the event if available
    tracker = models.ForeignKey(Tracker, related_name="triggered_events", blank=True, null=True)
    trigger = models.PositiveSmallIntegerField(
        _("trigger"), choices=TRIGGERS._zip("value", "label"))

    objects = RoundEventQuerySet.as_manager()

    def __str__(self):
        return "{!s} {!s}".format(self.tracker, self.get_trigger_display())
