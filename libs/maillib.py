import pytz
from datetime import datetime

from django.core.mail import send_mail
from django.template.loader import render_to_string

from subs.models import RedditLink
from django.template import Context


class MailLib(object):
    def build_context(self, member):
        ctx = dict()
        ctx['member'] = member
        ctx['rate'] = member.rate
        ctx['data'] = {}

        subscriptions = member.get_subscriptions()
        for subscription in subscriptions:
            limit = subscription.count
            title = subscription.subreddit

            qs_filter = {'subreddit__title': title}
            if member.rate == 'd':
                links = RedditLink.daily_links.filter(**qs_filter)[:limit]
            else:
                links = RedditLink.weekly_links.filter(**qs_filter)[:limit]
            ctx['data'][title] = links
        return ctx

    def minify(self, html_content):
        html_content = html_content.replace('  ', '')
        html_content = html_content.replace('\n', '')
        return html_content

    def sendmail(self, title, text_content, html_content, to):
        from_mail = 'Reddit.cool <no-reply@reddit.cool>'
        html_content = self.minify(html_content)

        send_mail(title, text_content, from_mail, to,
                  html_message=html_content)

    def send_weekly_mail(self, context, member):
        if datetime.now(pytz.utc).isoweekday != 1:
            """only send weekly mails at mondays, return otherwise"""
            return

        title = 'Top Reddit Links (Weekly)'
        html_content = render_to_string('email/template.html', context)
        text_content = render_to_string('email/template.txt', context)
        self.sendmail(title, text_content, html_content, [member.email])

    def send_daily_mail(self, context, member):
        title = 'Top Reddit Links (Daily)'
        html_content = render_to_string('email/template.html', context)
        text_content = render_to_string('email/template.txt', context)
        self.sendmail(title, text_content, html_content, [member.email])

    def process(self, member):
        ctx = self.build_context(member)
        context = Context(ctx)
        rate = member.rate

        if rate == 'w':
            self.send_weekly_mail(context, member)
        else:
            self.send_daily_mail(context, member)
