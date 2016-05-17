import graphene
from graphene import relay, resolve_only_args
from graphene.contrib.django import DjangoNode, DjangoObjectType
from graphene.contrib.django.debug import DjangoDebugPlugin
from graphene.contrib.django.filter import DjangoFilterConnectionField
from graphene.core.types.custom_scalars import DateTime

from . import models
from base_station.pilots import schema as pilot_schema
from base_station.utils.graphene.interfaces import TimeStampedInterface, SyncModelInterface


class RacePilot(SyncModelInterface, TimeStampedInterface, DjangoNode):

    pilot = relay.NodeField(pilot_schema.Pilot)

    class Meta:
        model = models.RacePilot


class Race(SyncModelInterface, TimeStampedInterface, DjangoNode):

    pilots = DjangoFilterConnectionField(pilot_schema.Pilot, description='All Pilots')
    # TODO: figure out how to work with m2m through models.
    # https://github.com/graphql-python/graphene/issues/83
    # pilots = DjangoFilterConnectionField(RacePilot, description='All Pilots')
    round_count = graphene.Int()
    rounds_remaining = graphene.Int()

    class Meta:
        model = models.Race

    def resolve_round_count(self, data, info, *args, **kwargs):
        return self.instance.rounds.count()

    def resolve_rounds_remaining(self, data, info):
        return self.instance.rounds.filter(ended_time__isnull=True).count()


class RoundEvent(SyncModelInterface, TimeStampedInterface, DjangoNode):

    trigger = graphene.Int()
    trigger_label = graphene.String()
    trigger_verbose_label = graphene.String()

    class Meta:
        model = models.RoundEvent

        filter_fields = {
            'trigger': ('exact',),
            'tracker': ('exact',)
        }

    def resolve_trigger_label(self, data, info):
        return models.RoundEvent.TRIGGERS(self.trigger).serializer_label

    def resolve_trigger_verbose_label(self, data, info):
        return models.RoundEvent.TRIGGERS(self.trigger).label


class Round(SyncModelInterface, TimeStampedInterface, DjangoNode):

    number = graphene.Int().NonNull
    goal_start_time = DateTime()
    goal_end_time = DateTime()
    started_time = DateTime()
    ended_time = DateTime()
    has_started = graphene.Boolean()
    has_ended = graphene.Boolean()
    event_template = graphene.String()
    state = graphene.Int()
    state_label = graphene.String()

    events = DjangoFilterConnectionField(RoundEvent, description='Round Race Events')

    class Meta:
        model = models.Round

    def resolve_state_label(self, data, info):
        return self.instance.STATES(self.state).label


class RaceQuery(graphene.ObjectType):
    race = relay.NodeField(Race)
    all_races = DjangoFilterConnectionField(Race, description='All Races')

    round = relay.NodeField(Round)
    all_rounds = DjangoFilterConnectionField(Round, description='All Race Rounds')

    event = relay.NodeField(RoundEvent)
    all_events = DjangoFilterConnectionField(RoundEvent, description='All Race Events')

    node = relay.NodeField()
    viewer = graphene.Field('self')

    def resolve_viewer(self, *args, **kwargs):
        # Currently we aren't filtering to only viewer specific data,
        # this is a stub to do that in the future.
        return self


schema = graphene.Schema(
    query=RaceQuery,
    name='Race details',
    # Currently causing issues
    # plugins=[DjangoDebugPlugin()]
)
