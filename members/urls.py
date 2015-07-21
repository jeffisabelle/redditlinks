from django.conf.urls import patterns, url
from members.views import ToWeekly, ToDaily, Unsubscribe

urlpatterns = patterns(
    '',
    url(r'^toweekly', ToWeekly.as_view(), name='toweekly'),
    url(r'^todaily', ToDaily.as_view(), name='todaily'),
    url(r'^unsubscribe', Unsubscribe.as_view(), name='unsubscribe'),
)
