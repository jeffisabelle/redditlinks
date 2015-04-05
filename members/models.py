from django.db import models


class Member(models.Model):
    email = models.EmailField()
    total_subscription = models.IntegerField(default=0)
    subscription = models.ManyToManyField(
        "Subscription",
        through="members.MemberSubscription"
    )
    is_active = models.NullBooleanField(default=False, null=True)

    def get_subscriptions(self):
        return self.subscription.all()

    def __unicode__(self):
        return self.email


class Subscription(models.Model):
    subreddit = models.CharField(max_length=200)
    count = models.IntegerField(default=5)

    def __unicode__(self):
        return "%s - %s" % (self.subreddit, self.count)

    class Meta:
        unique_together = (("subreddit", "count"),)


class MemberSubscription(models.Model):
    member = models.ForeignKey('members.Member')
    subscription = models.ForeignKey('members.Subscription')

    def __unicode__(self):
        return "%s - %s" % (self.subscription.subreddit, self.member.email)
