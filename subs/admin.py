from django.contrib import admin
from subs.models import RedditLink, Subreddit


class RedditLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'score', 'subreddit', 'parsed_at')
    list_filter = ('subreddit', 'parsed_at')
    ordering = ('-score', )

admin.site.register(RedditLink, RedditLinkAdmin)
admin.site.register(Subreddit)
