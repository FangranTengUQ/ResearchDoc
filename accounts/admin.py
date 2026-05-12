from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Subscription


class SubscriptionInline(admin.StackedInline):
    model = Subscription
    can_delete = False
    extra = 0


class CustomUserAdmin(UserAdmin):
    inlines = [SubscriptionInline]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'archived', 'created_at')
    list_filter = ('plan', 'archived')
    search_fields = ('user__username', 'user__email')
    list_per_page = 10
    actions = ['archive_subscriptions', 'unarchive_subscriptions']

    def archive_subscriptions(self, request, queryset):
        queryset.update(archived=True)
        self.message_user(request, f'{queryset.count()} subscription(s) archived.')
    archive_subscriptions.short_description = 'Archive selected subscriptions'

    def unarchive_subscriptions(self, request, queryset):
        queryset.update(archived=False)
        self.message_user(request, f'{queryset.count()} subscription(s) unarchived.')
    unarchive_subscriptions.short_description = 'Unarchive selected subscriptions'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
