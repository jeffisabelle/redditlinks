import pytz
from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template import Template, Context

from subs.models import RedditLink


class MailLib(object):
    def build_context(self, member):
        ctx = dict()
        ctx['member'] = member
        ctx['rate'] = member.rate
        ctx['host'] = settings.HOST
        ctx['data'] = {}

        subscriptions = member.get_subscriptions()
        for subscription in subscriptions:
            limit = subscription.count
            title = subscription.subreddit

            qs_filter = {'subreddit__title_iexact': title}
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

    def make_html_from_mjml(self, context, member, template):
        """
        not using this anymore as it creates too many processes.
        probably related w django-mjml version.
        """
        template_file = "email/daily.mjml"

        if template == "weekly":
            template_file = "email/weekly.mjml"

        mjml_content = render_to_string(template_file, context)
        mjml_before = "{% load mjml %}{% mjml %}"
        mjml_after = "{% endmjml %}"
        mjml_content = mjml_before + mjml_content + mjml_after

        # context already passed while bulding mjml
        new_context = Context()

        html_template = Template(mjml_content)
        return html_template.render(new_context)

    def send_weekly_mail(self, context, member):
        if datetime.now(pytz.utc).isoweekday() != 1:
            """only send weekly mails at mondays, return otherwise"""
            return

        today = datetime.now().strftime('%d %b %Y')
        title = 'Weekly Reddit Links - %s' % today
        # html_content = self.make_html_from_mjml(context, member, "daily")
        html_content = render_to_string('email/weekly.html', context)
        text_content = render_to_string('email/template.txt', context)
        self.sendmail(title, text_content, html_content, [member.email])

    def send_daily_mail(self, context, member):
        today = datetime.now().strftime('%d %b %Y')
        title = 'Daily Reddit Links - %s' % today
        # html_content = self.make_html_from_mjml(context, member, "weekly")
        html_content = render_to_string('email/daily.html', context)
        text_content = render_to_string('email/template.txt', context)
        self.sendmail(title, text_content, html_content, [member.email])

    def send_activation_mail(self, context, member):
        title = 'Welcome to reddit.cool newsletter'
        # html_content = self.make_html_from_mjml(context, member, "weekly")
        html_content = render_to_string('email/activation.html', context)
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
