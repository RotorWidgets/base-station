from graphene import relay
from graphene.contrib.django import DjangoNode

from . import models
from base_station.utils.graphene.interfaces import SyncModelInterface


class User(SyncModelInterface, DjangoNode):

    class Meta:
        model = models.User
