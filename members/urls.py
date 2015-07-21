from django.conf.urls import patterns, url
from members.views import ToWeekly, ToDaily

urlpatterns = patterns(
    '',
    url(r'^toweekly', ToWeekly.as_view(), name='toweekly'),
    url(r'^todaily', ToDaily.as_view(), name='todaily'),
)
