from django.contrib import admin

from follow.models import Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('to_user_follows', 'from_user_follows', 'created_at')
    list_filter = ('to_user_follows', 'from_user_follows')
    search_fields = ('to_user_follows', 'from_user_follows')
