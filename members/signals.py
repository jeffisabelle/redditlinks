from django.db.models.signals import post_save
from members.models import MemberSubscription


def update_subscription_count(sender, **kwargs):
    """
    when a new subscription saved for a member,
    we update the subscription count for the member with
    this signal.
    """
    instance = kwargs.get('instance')
    member = instance.member
    subs_count = MemberSubscription.objects.filter(member=member).count()
    instance.member.total_subscription = subs_count
    instance.member.save()


post_save.connect(update_subscription_count, sender=MemberSubscription)
