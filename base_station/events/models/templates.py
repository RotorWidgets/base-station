from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import (
    AutoSlugField
)
from django_extensions.db.models import (
    TitleSlugDescriptionModel,
    TimeStampedModel
)
from simple_history.models import HistoricalRecords


from base_station.utils.models import SyncModel


class EventTemplate(SyncModel, TimeStampedModel):
    """
    Dictates the logic that is used when running a race.
    """

    name = models.CharField(_("name"), max_length=255, default="")
    slug = AutoSlugField(_("slug"), populate_from="name")
    creator = models.ForeignKey("users.User", blank=True, null=True)
    # May have to store creator details in non FK way due to future sync issues?

    history = HistoricalRecords()

    def __str__(self):
        return self.title


class Timer(SyncModel):
    """
    Timer model to hold different designated times to trigger events
    """

    name = models.CharField(_("name"), max_length=255)
    slug = AutoSlugField(_("slug"), populate_from="name")
    duration = models.DurationField()
    tempalte = models.ForeignKey(EventTemplate)

    history = HistoricalRecords()


# class
