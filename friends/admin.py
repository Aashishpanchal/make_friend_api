from django.contrib import admin
from friends.models import Friend, SendFriendRequest


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    pass


@admin.register(SendFriendRequest)
class SendFriendRequestAdmin(admin.ModelAdmin):
    pass
