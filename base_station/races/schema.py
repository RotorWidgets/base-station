import graphene
from graphene import relay, resolve_only_args
from graphene.contrib.django import DjangoNode, DjangoObjectType
from graphene.contrib.django.debug import DjangoDebugPlugin
from graphene.contrib.django.filter import DjangoFilterConnectionField
from graphene.core.types.custom_scalars import DateTime

from . import models
from base_station.pilots.schema import Pilot
from base_station.utils.graphene.interfaces import TimeStampedInterface, SyncModelInterface


class RacePilot(SyncModelInterface, TimeStampedInterface, DjangoNode):

    class Meta:
        model = models.RacePilot


class Race(SyncModelInterface, TimeStampedInterface, DjangoNode):

    heats = DjangoFilterConnectionField(RacePilot, description='All Pilot Heats')

    class Meta:
        model = models.Race


class RoundEvent(SyncModelInterface, TimeStampedInterface, DjangoNode):

    trigger = graphene.Int()
    trigger_label = graphene.String()
    trigger_verbose_label = graphene.String()

    class Meta:
        model = models.RoundEvent

        filter_fields = {
            'trigger': ('exact',)
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
    active = graphene.Boolean()
    started = graphene.Boolean()
    ended = graphene.Boolean()
    event_template = graphene.String()

    events = DjangoFilterConnectionField(RoundEvent, description='Round Race Events')

    class Meta:
        model = models.Round

    # May not be needed?
    @classmethod
    def get_node(cls, _id, info):
        return Round(models.Round.objects.get(_id))


class RaceQuery(graphene.ObjectType):
    race = relay.NodeField(Race)
    all_races = DjangoFilterConnectionField(Race, description='All Races')

    round = relay.NodeField(Round)
    all_rounds = DjangoFilterConnectionField(Round, description='All Race Rounds')

    event = relay.NodeField(RoundEvent)
    all_events = DjangoFilterConnectionField(RoundEvent, description='All Race Events')

    node = relay.NodeField()
    viewer = graphene.Field('self')

    num_rounds = graphene.Int()

    def resolve_viewer(self, *args, **kwargs):
        # Currently we aren't filtering to only viewer specific data,
        # this is a stub to do that in the future.
        return self

    def resolve_num_rounds(self, *args, **kwargs):
        return models.Round.objects.all().count()

    def resolve_num_rounds(self, *args, **kwargs):
        return models.Round.objects.filter(ended_time__isnull=True).count()


schema = graphene.Schema(
    query=RaceQuery,
    name='Race details',
    # Currently causing issues
    # plugins=[DjangoDebugPlugin()]
)
