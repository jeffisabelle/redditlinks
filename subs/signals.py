from django.dispatch import Signal, receiver

from members.models import Member
from subs.utils.mails import MailCore
from subs.models import RedditLink

from datetime import date, timedelta

send_mails = Signal()


def get_qs_filter(rate):
    today = date.today()
    last_week = today - timedelta(days=7)

    if rate == 'd':
        qs_filter = {
            'parsed_at__year': today.year,
            'parsed_at__month': today.month,
            'parsed_at__day': today.day
        }
        return qs_filter

    qs_filter = {'parsed_at__range': [last_week, today]}
    return qs_filter


@receiver(send_mails)
def send_daily_mails(sender, **kwargs):
    print "starting to sending emails"

    rate = kwargs['rate']
    qs_filter = get_qs_filter(rate)

    mail_utils = MailCore()

    members = Member.objects.filter(is_active=True, rate=rate)
    for member in members:
        ctx = dict()
        ctx['member'] = member
        ctx['data'] = {}

        subscriptions = member.get_subscriptions()
        for subscription in subscriptions:
            limit = subscription.count
            title = subscription.subreddit

            links = RedditLink.objects.filter(
                subreddit__title=title, **qs_filter)[:limit]
            ctx['data'][title] = links

        mail_utils.process(ctx, rate)
        print 'sending mail - %s' % member

    print "emails sent"
