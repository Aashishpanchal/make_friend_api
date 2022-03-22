from rest_framework import serializers

from follow.models import Follow
from utility.serializers import ReadOnlyModelSerializer
from auth_user.api.user_serializers import UserDetailRetrieveSerializer

from auth_user.models import User


class FollowIDSerializer(serializers.Serializer):
    followed = serializers.UUIDField(required=True, allow_null=False)

    def validate_followed(self, value):
        """
        Check if the user_id is valid
        """
        try:
            self.followed_user_obj = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("user does not exist")
        return value


class FollowNowSerializer(FollowIDSerializer):
    """
        Serializer for Follow
    """

    def validate_followed(self, value):
        super().validate_followed(value)
        try:
            Follow.objects.get(
                user=self.context["request"].user, followed=self.followed_user_obj)
            raise serializers.ValidationError("You already follow this user")
        except Follow.DoesNotExist:
            pass
        return value

    def create(self, validated_data):
        """
        Create a new Follow instance
        """
        user = self.context["request"].user
        return Follow.objects.create(
            user=user, followed=self.followed_user_obj)


class UserDetailRetrieveSerializer(UserDetailRetrieveSerializer):
    """
        Only Read Data from User, We cannot change it
    """
    class Meta(UserDetailRetrieveSerializer.Meta):
        fields = ("id", "username", "email", "first_name",
                  "last_name", "user_image")


class FollowRetrieveSerializer(ReadOnlyModelSerializer):
    """
        Serializer for Follow
    """
    followed = UserDetailRetrieveSerializer()

    class Meta:
        model = Follow
        fields = ("id", "followed", "created_at")
