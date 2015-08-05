from django.conf.urls import patterns, url
from subs.views import SubredditList

urlpatterns = patterns(
    '',
    url(r'^subreddits/json/$', SubredditList.as_view(),
        name='subreddits-json'),
)
