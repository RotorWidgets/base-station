import uuid

from django.db import models


class SyncModel(models.Model):
    """
    A model that can be synced between the base station and the sync web service
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
