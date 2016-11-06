import json
import urllib

from members.models import Member, Subscription, MemberSubscription
from libs.maillib import MailLib
from subs.models import Subreddit

import pytz
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView, View
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


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

    def activate(self, member):
        member.is_active = True
        member.save()
        return member


class TimezoneList(View):
    def get(self, request, *args, **kwargs):
        commons = pytz.common_timezones
        data = {}
        data["timezones"] = commons
        return JsonResponse(data)


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


class Activate(TemplateView, MemberUpdateView):
    template_name = 'members/activate.html'

    def get_context_data(self, **kwargs):
        context = super(Activate, self).get_context_data(**kwargs)

        member = self.get_member()
        self.activate(member)

        context['member'] = member
        context['host'] = settings.HOST
        return context


class Complete(TemplateView, MemberUpdateView):
    template_name = 'members/complete-registeration.html'

    def get_context_data(self, **kwargs):
        context = super(Complete, self).get_context_data(**kwargs)

        member = self.get_member()
        context['member'] = member
        context['host'] = settings.HOST
        ml = MailLib()
        ml.send_activation_mail(context, member)

        return context


class PreferencesView(TemplateView, MemberUpdateView):
    template_name = 'members/preferences.html'

    def get_context_data(self, **kwargs):
        context = super(PreferencesView, self).get_context_data(**kwargs)
        member = self.get_member()
        context['member'] = member
        context['host'] = settings.HOST
        return context


class PreferencesRegisterationView(PreferencesView):
    template_name = 'members/preferences-registeration.html'


class PreferencesUpdateView(MemberUpdateView):
    """
    dont use csrf_exampt, pass csrf to the template
    with PreferenceView, then use DJANGO_VARS to save
    it to javascript, then use csrf variable in react.
    """
    def update_member_subscription(self, member, subreddit, count):
        subreddit, created = Subreddit.objects.get_or_create(title=subreddit)
        subscription, created = Subscription.objects.get_or_create(
            subreddit=subreddit, count=count)
        ms, created = MemberSubscription.objects.get_or_create(
            member=member, subscription=subscription)
        return

    def get(self, request, *args, **kwargs):
        member = self.get_member()
        member_subscriptions = MemberSubscription.objects.select_related(
            "member", "subscription").filter(member=member)

        data = []
        for sub in member_subscriptions:
            subscription = {
                "subreddit": sub.subscription.subreddit,
                "count": sub.subscription.count
            }
            data.append(subscription)
        return JsonResponse({'data': data})

    def post(self, request, *args, **kwargs):
        member = self.get_member()
        request = json.loads(request.body)
        MemberSubscription.objects.filter(member=member).delete()
        for data in request:
            subreddit = data["subreddit"]
            count = int(data["count"])
            self.update_member_subscription(member, subreddit, count)

        return JsonResponse({"status": "ok"})

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(PreferencesUpdateView, self).dispatch(*args, **kwargs)


class Register(View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        email = data.get("email")
        dwswitch = data.get("dailyweeklyswitch")
        timezone = data.get("timezone")

        if dwswitch == "on":
            switch = "d"
        else:
            switch = "w"

        member, created = Member.objects.get_or_create(
            email=email, rate=switch, timezone=timezone)

        if not created:
            print "user already registered"
            return redirect("/")

        params = {
            "member": member.member_uuid,
            "token": member.member_token,
            "registeration": "yes"
        }
        params = urllib.urlencode(params)
        path = reverse("preferences-register") + "?" + params

        return redirect(path)
