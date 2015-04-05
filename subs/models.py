from django.db import models


class RedditLink(models.Model):
    title = models.CharField(max_length=500, null=True)
    url = models.URLField(max_length=500, null=True)
    domain = models.CharField(max_length=200, null=True)
    score = models.IntegerField(null=True)
    comments_permalink = models.URLField(max_length=500, unique=True)
    comments_count = models.IntegerField(null=True)
    subreddit = models.ForeignKey('Subreddit')
    author = models.CharField(max_length=200, null=True)
    parsed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']

    def __unicode__(self):
        return self.title


class Subreddit(models.Model):
    title = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title
