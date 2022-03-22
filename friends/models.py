import uuid
from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class SendFriendRequest(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False, serialize=False)
    # who is sending this request
    from_user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="from_user")
    # who is receiving this request
    to_user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="to_user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.from_user.username + " -> " + self.to_user.username

    class Meta:
        ordering = ["-created_at"]


class Friend(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False, serialize=False)
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="user_at")
    friend = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="user_friends")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + " <-+-> " + self.friend.username

    class Meta:
        ordering = ["-created_at"]
