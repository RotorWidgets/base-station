import graphene
from graphene.core.types.custom_scalars import DateTime


class SyncModelInterface(graphene.Interface):
    pass


class TimeStampedInterface(graphene.Interface):

    created = DateTime()
    modified = DateTime()
