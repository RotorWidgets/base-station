from graphene import relay
from graphene.contrib.django import DjangoNode

from . import models
from base_station.users.schema import User
from base_station.utils.graphene.interfaces import SyncModelInterface


class Pilot(SyncModelInterface, DjangoNode):

    user = relay.NodeField(User)

    class Meta:
        model = models.Pilot
