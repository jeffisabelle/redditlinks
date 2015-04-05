from django.dispatch import Signal, receiver

from members.models import Member
from subs.utils.mails import MailCore
from subs.models import Subreddit, RedditLink

from datetime import date

parsing_done = Signal()


@receiver(parsing_done)
def parsing_done_callback(sender, **kwargs):
    print "starting to sending emails"
    mail_utils = MailCore()
    today = date.today()

    members = Member.objects.filter(is_active=True)
    for member in members:
        ctx = dict()
        ctx['member'] = member
        ctx['data'] = {}

        subscriptions = member.get_subscriptions()
        for subscription in subscriptions:
            limit = subscription.count
            subreddit = Subreddit.objects.get(title=subscription.subreddit)

            links = RedditLink.objects.filter(
                subreddit=subreddit, parsed_at__year=today.year,
                parsed_at__month=today.month, parsed_at__day=today.day)[:limit]
            ctx['data'][subreddit] = links

        mail_utils.process(ctx)
        print 'sending mail - %s' % member
    print "emails sent"

if __name__ == '__main__':
    parsing_done.send(sender=None)
