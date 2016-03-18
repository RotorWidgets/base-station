from django.conf.urls import url

from events.views import (
    EventDetailViewBase, UpcomingOccurrencesViewBase,
    OccurrenceDetailViewBase, OccurrenceUpdateViewBase, OccurrenceDeleteViewBase)


urlpatterns = (
    url(r'upcoming$', UpcomingOccurrencesViewBase.as_view(), name='upcoming'),
    # occurrence views
    url(r'^(?P<pk>\d+)/$',
        EventDetailViewBase.as_view(),
        name='detail'),
    url(r'^(?P<pk>\d+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        OccurrenceDetailViewBase.as_view(),
        name='occurrence_detail'),
    url(r'^(?P<pk>\d+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/update/$',
        OccurrenceUpdateViewBase.as_view(),
        name='occurrence_update'),
    url(r'^(?P<pk>\d+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/delete/$',
        OccurrenceDeleteViewBase.as_view(),
        name='occurrence_delete'),
)
