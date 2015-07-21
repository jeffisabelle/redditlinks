from members.models import Member
from django.views.generic.base import TemplateView, View
from django.shortcuts import get_object_or_404
from django.conf import settings


class MemberUpdateView(View):
    def get_member(self):
        uuid = self.request.GET['member']
        token = self.request.GET['token']
        return get_object_or_404(Member, member_uuid=uuid, member_token=token)

    def update_member_rate(self, member, new_rate):
        member.rate = new_rate
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
