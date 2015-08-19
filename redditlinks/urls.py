from django.conf.urls import patterns, include, url
from django.contrib import admin
from redditlinks.views import ExampleMail, Homepage, yandex_confirmation

"""
Examples:
url(r'^$', 'redditlinks.views.home', name='home'),
url(r'^blog/', include('blog.urls')),
"""

urlpatterns = patterns(
    '', url(r'^admin/', include(admin.site.urls)),
    url('^$', Homepage.as_view(), name='homepage'),
    url('^69b906256894.html$', yandex_confirmation, name='yandex'),
    url('^members/', include('members.urls')),
    url('^subs/', include('subs.urls')),
    url('^example-mail/', ExampleMail.as_view(), name='examplemail'),
)
