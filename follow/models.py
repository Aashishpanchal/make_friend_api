import uuid
from django.db import models

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Follow(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False, serialize=False)
    from_user_follows = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="from_user_follows")
    to_user_follows = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="to_user_follows")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<{class_name}(id: {_id}, from_user_follows: {from_user_follows}, to_user_follows: {to_user_follows})>".format(
            class_name=self.__class__.__name__,
            _id=self.id,
            from_user_follows=self.from_user_follows.username,
            to_user_follows=self.to_user_follows.username
        )
