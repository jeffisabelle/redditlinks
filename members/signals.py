from django.db.models.signals import post_save
from members.models import MemberSubscription, Member


def update_subscription_count(sender, **kwargs):
    """

    Arguments:
    - `sender`:
    - `**kwargs`:
    """

    instance = kwargs.get('instance')
    instance.member.total_subscription = MemberSubscription.objects.filter(
        member=instance.member
    ).count()
    instance.member.save()


post_save.connect(update_subscription_count, sender=MemberSubscription)
