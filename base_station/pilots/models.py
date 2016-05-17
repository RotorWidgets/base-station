from django.db import models
from django.utils.translation import ugettext_lazy as _

from base_station.utils.models import SyncModel
from base_station.users.models import User


class Pilot(SyncModel):
    """Store details related to a pilot"""

    callsign = models.CharField(_('Moniker/Callsign'), blank=True, max_length=100)
    # optional relationship to a user
    user = models.ForeignKey(User, blank=True, null=True)

    def __str__(self):
        if self.user:
            return "{} ({})".format(self.callsign, (self.user.name or self.user))
        return "{}".format(self.callsign)
