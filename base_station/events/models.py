from django.db import models
from django_extensions.db.models import (
    TitleSlugDescriptionModel,
    TimeStampedModel
)
from simple_history.models import HistoricalRecords


from base_station.utils.models import UUIDModel


class EventTemplate(UUIDModel, TitleSlugDescriptionModel, TimeStampedModel):
    """
    Dictates the logic that is used when running a race.
    """
    history = HistoricalRecords()

    def __str__(self):
        return self.title


# Should models that are related to event design be included in the models here?

# Timer model to hold different designated times to trigger an esettings

class Event(UUIDModel, TitleSlugDescriptionModel, TimeStampedModel):

    template = models.ForeignKey(EventTemplate)

    history = HistoricalRecords()

    def __str__(self):
        return self.title
