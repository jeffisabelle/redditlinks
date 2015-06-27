from django.conf.urls import patterns, url
from members.views import ToWeekly

urlpatterns = patterns(
    '',
    url(r'^toweekly', ToWeekly.as_view(), name='toweekly'),
)
