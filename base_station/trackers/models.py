from catalog import Catalog
from django.db import models
from django_extensions.db.models import TimeStampedModel

from base_station.utils.models import SyncModel


class TRACKER_TYPES(Catalog):
    _attrs = ('value', 'label', 'serializer_label')
    unknown = (0, 'Unkown', 'unknown')
    rw_transponder = (1, 'Rotor Widgets Transponder v1', 'rw_transponder_v1')
    ilap = (2, 'iLap', 'ilap')


class Tracker(SyncModel, TimeStampedModel):
    """
    Represents a peices of tracker hardware that is transmitting from a vehicle.
    There can be multiple trackers with the same transmitting ID or the like.
    However the race should perform a check to make sure no Tracker has the same ID.
    Unique to a racer, has the possibility to change during a race if one
    breaks and a racer needs a new one assigned. In the future maybe support
    updating the tracker's transmitting ID dynamically on supporting hardware.
    """

    transponder_id = models.IntegerField(blank=True, null=True)
    tracker_type = models.PositiveSmallIntegerField(
        choices=TRACKER_TYPES._zip('value', 'label'),
        default=TRACKER_TYPES.unknown.value)

    def __str__(self):
        return "{!s} - {!s}".format(self.transponder_id, self.get_tracker_type_display())
