import graphene
from graphene import relay, resolve_only_args
from graphene.contrib.django import DjangoNode, DjangoObjectType
from graphene.contrib.django.filter import DjangoFilterConnectionField
from graphene.core.types.custom_scalars import DateTime

from .models import RaceHeat, HeatEvent
from base_station.utils.interfaces import TimeStampedInterface


schema = graphene.Schema(name='Race details')


class RaceHeatNode(TimeStampedInterface, DjangoNode):

    number = graphene.Int().NonNull
    # event = FK
    started_time = DateTime()
    ended_time = DateTime()
    started = graphene.Boolean()
    ended = graphene.Boolean()
    event_template = graphene.String()

    # events = DjangoFilterConnectionField(HeatEventNode, description='Heat Race Events')

    class Meta:
        model = RaceHeat

    @classmethod
    def get_node(cls, _id, info):
        return RaceHeatNode(RaceHeat.objects.get(_id))


class HeatEventNode(TimeStampedInterface, DjangoNode):

    heat = relay.NodeField(RaceHeatNode)

    trigger = graphene.Int()
    trigger_label = graphene.String()
    trigger_verbose_label = graphene.String()


    class Meta:
        model = HeatEvent

        filter_fields = {
            'trigger': ('exact',)
        }

    def resolve_trigger_label(self, data, info):
        return HeatEvent.TRIGGERS(self.trigger).serializer_label

    def resolve_trigger_verbose_label(self, data, info):
        return HeatEvent.TRIGGERS(self.trigger).label


class RaceQuery(graphene.ObjectType):
    heat = relay.NodeField(RaceHeatNode)
    all_heats = DjangoFilterConnectionField(RaceHeatNode, description='All Race Heats')

    event = relay.NodeField(HeatEventNode)
    all_events = DjangoFilterConnectionField(HeatEventNode, description='All Race Events')


schema.query = RaceQuery
