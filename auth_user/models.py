import uuid

from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser as DjangoAbstractUser

from auth_user.utils import (
    user_image_path,
    user_default_image,
    user_back_cover_image_path,
    user_default_back_cover_image
)
from auth_user.manager import CustomUserManager


class AbstractUser(DjangoAbstractUser):
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False, serialize=False)
    user_image = models.ImageField(_("User Profile Image"), upload_to=user_image_path,
                                   default=user_default_image)
    back_cover_image = models.ImageField(
        upload_to=user_back_cover_image_path, default=user_default_back_cover_image, blank=True)
    bio = models.TextField(max_length=160, blank=True, null=True)

    objects = CustomUserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return str(self.id)


class User(AbstractUser):
    class Meta:
        swappable = 'AUTH_USER_MODEL'
        db_table = 'auth_user'

    @property
    def full_name(self):
        user_fullname = self.get_full_name()
        return user_fullname

    def followers(self):
        try:
            return self.follow_followed.count()
        except Exception as e:
            return 0

    def following(self):
        try:
            return self.follow_follower.count()
        except Exception as e:
            return 0
