"""
Race templates contain configuration and options that are used when a race
is run.
Options are overwritable by individual races
"""
from catalog import Catalog
from django.contrib.postgres.fields import JSONField
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


class RaceType(SyncModel):
    """
    Race Types
    """
    name = models.CharField(_("name"), max_length=255, default="")
    slug = AutoSlugField(_("slug"), populate_from="name")
    # creator = models.ForeignKey("users.User", blank=True, null=True)
    default_options = models.OneToOneField('RaceOptions')

    def __str__(self):
        return "{} type".format(self.name)


class RaceOptions(SyncModel):
    options = JSONField()

    class Meta:
        verbose_name = _('Race Options')
        verbose_name_plural = _('Race Options')

    def __str__(self):
        return "options {!s}".format(self.options)


    # def __getattr__(self, key):
    #     try:
    #         return self.options[key]
    #     except KeyError:
    #         raise AttributeError(key)
    #
    # def __setattr__(self, key, value):
    #     self.options[key] = value
    #
    # def __dir__(self):
    #     return self.options.keys()


class RaceTemplate(SyncModel, TimeStampedModel):
    """
    Dictates the logic that is used when running a race.
    """

    name = models.CharField(_("name"), max_length=255, default="")
    slug = AutoSlugField(_("slug"), populate_from="name")
    # May have to store creator details in non FK way due to future sync issues?
    creator = models.ForeignKey("users.User", blank=True, null=True)
    type = models.ForeignKey(RaceType)
    options = models.OneToOneField(RaceOptions)

    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Timer(SyncModel):
    """
    Timer model to hold different designated times to trigger events during a race
    """

    name = models.CharField(_("name"), max_length=255)
    slug = AutoSlugField(_("slug"), populate_from="name")
    duration = models.DurationField()
    template = models.ForeignKey(RaceTemplate)

    history = HistoricalRecords()
