import uuid

from django.db import models
import pytz


class Member(models.Model):
    RATE_CHOICES = (
        ('d', 'Daily'),
        ('w', 'Weekly'),
    )

    TYPE_CHOICES = (
        ('freemium', 'Freemium'),
        ('premium', 'Premium'),
        ('special', 'Special'),
    )

    ZONE_CHOICES = tuple([(zone, zone) for zone in pytz.all_timezones])

    email = models.EmailField()
    member_uuid = models.UUIDField(default=uuid.uuid4, editable=True)
    member_token = models.UUIDField(default=uuid.uuid4, editable=True)
    total_subscription = models.IntegerField(default=0)
    subscription = models.ManyToManyField(
        "Subscription", through="members.MemberSubscription")
    is_active = models.NullBooleanField(default=False, null=True)
    rate = models.CharField(max_length=1, default='d', null=True,
                            choices=RATE_CHOICES)
    timezone = models.CharField(null=True, blank=True, max_length=50,
                                choices=ZONE_CHOICES)
    subscription_type = models.CharField(
        default='freemium', max_length=10, choices=TYPE_CHOICES)

    def get_subscriptions(self):
        return self.subscription.all()

    def __unicode__(self):
        return self.email

    class Meta:
        app_label = 'members'


class Subscription(models.Model):
    subreddit = models.CharField(max_length=200)
    count = models.IntegerField(default=5)

    def __unicode__(self):
        return "%s - %s" % (self.subreddit, self.count)

    class Meta:
        unique_together = (("subreddit", "count"),)
        app_label = 'members'


class MemberSubscription(models.Model):
    member = models.ForeignKey('members.Member')
    subscription = models.ForeignKey('members.Subscription')

    def __unicode__(self):
        return "%s - %s" % (self.subscription.subreddit, self.member.email)

    class Meta:
        app_label = 'members'
