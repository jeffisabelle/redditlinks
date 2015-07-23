from members.models import Member, MemberSubscription

from django.views.generic.base import TemplateView, View
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import JsonResponse


class MemberUpdateView(View):
    def get_member(self):
        uuid = self.request.GET['member']
        token = self.request.GET['token']
        return get_object_or_404(Member, member_uuid=uuid, member_token=token)

    def update_member_rate(self, member, new_rate):
        member.rate = new_rate
        member.save()
        return member

    def unsubscribe(self, member):
        member.is_active = False
        member.save()
        return member


class ToWeekly(TemplateView, MemberUpdateView):
    template_name = 'members/toweekly.html'

    def get_context_data(self, **kwargs):
        context = super(ToWeekly, self).get_context_data(**kwargs)

        member = self.get_member()
        self.update_member_rate(member, "w")

        context['member'] = member
        context['host'] = settings.HOST
        return context


class ToDaily(TemplateView, MemberUpdateView):
    template_name = 'members/todaily.html'

    def get_context_data(self, **kwargs):
        context = super(ToDaily, self).get_context_data(**kwargs)

        member = self.get_member()
        self.update_member_rate(member, "d")

        context['member'] = member
        context['host'] = settings.HOST
        return context


class Unsubscribe(TemplateView, MemberUpdateView):
    template_name = 'members/unsubscribe.html'

    def get_context_data(self, **kwargs):
        context = super(Unsubscribe, self).get_context_data(**kwargs)

        member = self.get_member()
        self.unsubscribe(member)

        context['member'] = member
        context['host'] = settings.HOST
        return context


class PreferencesView(TemplateView, MemberUpdateView):
    template_name = 'members/preferences.html'

    def get_context_data(self, **kwargs):
        context = super(PreferencesView, self).get_context_data(**kwargs)
        member = self.get_member()
        context['member'] = member
        context['host'] = settings.HOST
        return context


class PreferencesUpdateView(MemberUpdateView):

    def get(self, request, *args, **kwargs):
        member = self.get_member()
        member_subscriptions = MemberSubscription.objects.select_related(
            "member", "subscription").filter(member=member)

        data = []
        for sub in member_subscriptions:
            subscription = {
                "subreddit": sub.subscription.subreddit,
                "count": sub.subscription.count,
                "id": sub.subscription.id
            }
            data.append(subscription)
        return JsonResponse({'data': data})
