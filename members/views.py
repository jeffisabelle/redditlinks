from members.models import Member
from django.views.generic.base import TemplateView, View
from django.shortcuts import get_object_or_404
from django.conf import settings


class MemberUpdateView(View):
    def get_member(self):
        uuid = self.request.GET['member']
        token = self.request.GET['token']
        return get_object_or_404(Member, member_uuid=uuid, member_token=token)


class ToWeekly(TemplateView, MemberUpdateView):
    template_name = 'members/toweekly.html'

    def get_context_data(self, **kwargs):
        context = super(ToWeekly, self).get_context_data(**kwargs)
        context['member'] = self.get_member()
        context['host'] = settings.HOST
        return context
