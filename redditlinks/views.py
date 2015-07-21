from django.conf import settings
from django.views.generic.base import TemplateView
from subs.models import RedditLink
from members.models import Member


class Homepage(TemplateView):
    template_name = "home.html"


class ExampleMail(TemplateView):
    template_name = "email/weekly.html"

    def get_context_data(self, **kwargs):
        context = super(ExampleMail, self).get_context_data(**kwargs)
        # context['latest_articles'] = Article.objects.all()[:5]
        member = Member.objects.get(email='muhitosan@gmail.com')
        context['member'] = member
        context['data'] = {}
        context['host'] = settings.HOST

        subscriptions = member.get_subscriptions()
        for subscription in subscriptions:
            limit = subscription.count
            title = subscription.subreddit
            qs_filter = {'subreddit__title': title}
            links = RedditLink.objects.filter(**qs_filter)[:limit]
            context['data'][title] = links

        return context
