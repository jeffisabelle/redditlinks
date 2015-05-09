from django.conf.urls import patterns, include, url
from django.contrib import admin
from redditlinks.views import ExampleMail

"""
Examples:
url(r'^$', 'redditlinks.views.home', name='home'),
url(r'^blog/', include('blog.urls')),
"""

urlpatterns = patterns(
    '', url(r'^admin/', include(admin.site.urls)),
    url('^example-mail/', ExampleMail.as_view(), name='examplemail'),
)
