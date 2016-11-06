from django.conf.urls import patterns, url
from members.views import (
    ToWeekly, ToDaily, Unsubscribe, Register, PreferencesView, TimezoneList,
    PreferencesUpdateView, PreferencesRegisterationView, Activate, Complete)

urlpatterns = patterns(
    '',
    url(r'^toweekly', ToWeekly.as_view(), name='toweekly'),
    url(r'^todaily', ToDaily.as_view(), name='todaily'),
    url(r'^unsubscribe', Unsubscribe.as_view(), name='unsubscribe'),
    url(r'^activate', Activate.as_view(), name='activate'),
    url(r'^complete$', Complete.as_view(), name='complete-registeration'),
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'^preferences$', PreferencesView.as_view(), name='preferences'),
    url(r'^preferences-register$', PreferencesRegisterationView.as_view(),
        name='preferences-register'),
    url(r'^preferences.*/json/$', PreferencesUpdateView.as_view(),
        name='preferences-json'),
    url(r'^timezones/json/$', TimezoneList.as_view(),
        name='timezones-json'),
)
