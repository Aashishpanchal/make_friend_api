import uuid
from django.db import models

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Follow(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False, serialize=False)
    user = models.ForeignKey(
        UserModel, related_name='follow_follower', on_delete=models.CASCADE)
    followed = models.ForeignKey(
        UserModel, related_name='follow_followed', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' follows ' + self.followed.username
