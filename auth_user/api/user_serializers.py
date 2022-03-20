from rest_framework import serializers
from rest_framework import exceptions as api_exceptions
from rest_framework.settings import api_settings

from django.db import IntegrityError, transaction
from django.contrib.auth.password_validation import validate_password

from auth_user.models import User
from auth_user.constants import Messages


class UserCreateSerializer(serializers.ModelSerializer):
    default_error_messages = {
        "cannot_create_user": Messages.CANNOT_CREATE_USER,
    }

    class Meta:
        model = User
        fields = ("id", "username", "email",
                  "first_name", "last_name", "password",)
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"required": True, "write_only": True},
            "email": {"required": True},
        }

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except api_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                # no field error
                serializer_error[api_settings.NON_FIELD_ERRORS_KEY]
            )

        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")
        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
        return user


class UserCreatePasswordRetypeSerializer(UserCreateSerializer):
    default_error_messages = {
        "password_mismatch": Messages.PASSWORD_MISMATCH_ERROR
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["re_password"] = serializers.CharField(
            style={"input_type": "password"}
        )

    def validate(self, attrs):
        self.fields.pop("re_password", None)
        re_password = attrs.pop("re_password")
        password = attrs.get("password")
        if password == re_password:
            return super().validate(attrs)
        else:
            self.fail("password_mismatch")


class UserDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email",
                  "first_name", "last_name", "bio", "user_image", "back_cover_image")
        extra_kwargs = {
            "id": {"read_only": True},
            "email": {"read_only": True},
            "username": {"read_only": True},
            "user_image": {"required": False},
            "back_cover_image": {"required": False},
            "bio": {"required": False},
        }


class UserDetailRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'user_image', 'back_cover_image', 'bio']
        read_only_fields = ('id', 'username', 'email',
                            'first_name', 'last_name', 'user_image', 'back_cover_image', 'bio')
