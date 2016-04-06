import graphene
from graphene.core.types.custom_scalars import DateTime


class SyncModelInterface(graphene.Interface):
    """
    Field interface for Syncable models
    # TOOD: also include the synced state when implemented
    """
    uuid = graphene.String(description='UUID for this object')

    def resolve_uuid(self, data, info):
        return str(self.id)


class TimeStampedInterface(graphene.Interface):

    created = DateTime()
    modified = DateTime()
