from django.contrib import admin
from members.models import Member, Subscription, MemberSubscription


class SubscriptionAdmin(admin.ModelAdmin):
    """ Subscription admin display """
    list_display = ('subreddit', 'count')
    search_fields = ('subreddit', )


class MemberSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('member', 'subscription')
    list_filter = ('member', 'subscription')
    search_fields = ('subscription', )


class MemberSubscriptionInlineAdmin(admin.TabularInline):
    model = MemberSubscription


class MemberAdmin(admin.ModelAdmin):
    list_display = ('email', 'rate', 'is_active',
                    'total_subscription', 'timezone')
    list_filter = ('rate', 'is_active')

    inlines = [
        MemberSubscriptionInlineAdmin
    ]

admin.site.register(Member, MemberAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(MemberSubscription, MemberSubscriptionAdmin)
