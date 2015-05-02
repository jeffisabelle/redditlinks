from django.core.mail import send_mail
from django.template.loader import render_to_string

from members.models import Member
from subs.models import Subreddit, RedditLink
from django.template import Context
from datetime import date


class MailLib(object):
    def build_context(self, member):
        ctx = dict()
        ctx['member'] = member
        ctx['data'] = {}

        subscriptions = member.get_subscriptions()
        for subscription in subscriptions:
            limit = subscription.count
            title = subscription.subreddit

            qs_filter = {'subreddit__title': title}
            links = RedditLink.daily_links.filter(**qs_filter)[:limit]
            ctx['data'][title] = links
        return ctx

    def process(self, member, rate):
        ctx = self.build_context(member)
        context = Context(ctx)

        html_content = render_to_string('email/template.html', context)
        text_content = render_to_string('email/template.txt', context)

        if rate == 'w':
            title = 'Top Reddit Links (Weekly)'
        else:
            title = 'Top Reddit Links (Daily)'

        send_mail(title, text_content,
                  'Reddit.cool <no-reply@reddit.cool>',
                  [ctx['member'].email],
                  html_message=html_content)
