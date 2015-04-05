import os
import sys

project_folder = "redditlinks"
os.environ['DJANGO_SETTINGS_MODULE'] = 'redditlinks.settings'

if project_folder not in sys.path:
    sys.path.append("/Users/muhammetcan/projects/tahta/django/redditlinks")


from django.core.mail import send_mail
from django.template.loader import render_to_string

from members.models import Member
from subs.models import Subreddit, RedditLink
from django.template import Context
from datetime import date
import codecs


class MailCore():

    def test_data(self):
        members = Member.objects.all()
        today = date.today()

        for member in members:
            ctx = dict()
            ctx['member'] = member
            ctx['data'] = {}

            subscriptions = member.get_subscriptions()
            for subscription in subscriptions:
                limit = subscription.count
                subreddit = Subreddit.objects.get(
                    title=subscription.subreddit)
                links = RedditLink.objects.filter(
                    subreddit=subreddit, parsed_at__year=today.year,
                    parsed_at__month=today.month,
                    parsed_at__day=today.day)[:limit]
                ctx['data'][subreddit] = links

        return ctx

    def process(self, ctx):
        context = Context(ctx)

        html_content = render_to_string('email/template.html', context)
        text_content = render_to_string('email/template.txt', context)

        f = codecs.open('hede.html', 'w+', 'utf-8')
        f.write(html_content)
        f.close()

        # send_mail(
        #     'Top Reddit Links',
        #     text_content,
        #     'Reddit.cool <no-reply@reddit.cool>',
        #     [ctx['member'].email],
        #     html_message=html_content,
        # )

        # print ctx


if __name__ == '__main__':
    import django
    django.setup()

    m = MailCore()
    ctx = m.test_data()
    m.process(ctx)
    print 'ifmain done'
