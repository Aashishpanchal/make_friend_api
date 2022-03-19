import uuid
from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class SendFriendRequest(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False, serialize=False)
    from_user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="from_user_friend_requests")
    to_user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="to_user_friend_requests")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<{class_name}(id: {_id}, from_user: {from_user}, to_user: {to_user})>".format(
            class_name=self.__class__.__name__,
            _id=self.id,
            from_user=self.from_user.username,
            to_user=self.to_user.username
        )


class Friend(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False, serialize=False)
    friend = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="from_use_friends")
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="to_user_friends")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<{class_name}(id: {_id}, friend: {friend}, user: {user})>".format(
            class_name=self.__class__.__name__,
            _id=self.id,
            friend=self.friend.username,
            user=self.user.username
        )
