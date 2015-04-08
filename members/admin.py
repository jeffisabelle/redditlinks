from django.contrib import admin
from members.models import Member, Subscription, MemberSubscription


class SubscriptionAdmin(admin.ModelAdmin):
    """ Subscription admin display """
    list_display = ('subreddit', 'count')


class MemberSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('member', 'subscription')


class MemberAdmin(admin.ModelAdmin):
    list_display = ('email', 'rate', 'is_active', 'total_subscription')

admin.site.register(Member, MemberAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(MemberSubscription, MemberSubscriptionAdmin)
