from django.conf.urls import patterns, url
from members.views import (ToWeekly, ToDaily, Unsubscribe, Register,
                           PreferencesView, PreferencesUpdateView,
                           PreferencesRegisterationView)

urlpatterns = patterns(
    '',
    url(r'^toweekly', ToWeekly.as_view(), name='toweekly'),
    url(r'^todaily', ToDaily.as_view(), name='todaily'),
    url(r'^unsubscribe', Unsubscribe.as_view(), name='unsubscribe'),
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'^preferences$', PreferencesView.as_view(), name='preferences'),
    url(r'^preferences-register$', PreferencesRegisterationView.as_view(),
        name='preferences-register'),
    url(r'^preferences/json/$', PreferencesUpdateView.as_view(),
        name='preferences-json'),
)
