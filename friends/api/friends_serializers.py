from rest_framework import serializers

from auth_user.api.user_serializers import AllUserListSerializer
from auth_user.models import User
from friends.models import SendFriendRequest, Friend

from utility.serializers import ReadOnlyModelSerializer


class FriendIDSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(required=True, allow_null=False)

    def validate_user_id(self, value):
        """
        Check if the user_id is valid
        """
        try:
            self.user_obj = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("user does not exist")
        return value

    @property
    def data(self):
        return {
            'user_id': self.user_obj.id
        }


class SendFriendRequestSerializer(FriendIDSerializer):
    """
        Serializer for SendFriendRequest
    """

    def validate_user_id(self, value):
        value = super().validate_user_id(value)
        try:
            SendFriendRequest.objects.get(
                from_user=self.context["request"].user, to_user=self.user_obj)
            raise serializers.ValidationError(
                "You already send a friend request to this user")
        except SendFriendRequest.DoesNotExist:
            try:
                Friend.objects.get(
                    user=self.context["request"].user, friend=self.user_obj)
                raise serializers.ValidationError(
                    "You are already friends with this user")
            except Friend.DoesNotExist:
                pass
        return value

    def create(self, validated_data):
        """
        Create a new SendFriendRequest instance
        """
        return SendFriendRequest.objects.create(
            from_user=self.context["request"].user,
            to_user=self.user_obj
        )


class FriendRequestAcceptSerializer(FriendIDSerializer):
    """
        Serializer for AcceptFriendRequest
    """

    def validate_user_id(self, value):
        value = super().validate_user_id(value)
        try:
            self.friend_request_obj = SendFriendRequest.objects.get(
                from_user=self.context["request"].user, to_user=self.user_obj)
        except SendFriendRequest.DoesNotExist:
            try:
                Friend.objects.get(
                    user=self.context["request"].user, friend=self.user_obj)
                raise serializers.ValidationError(
                    "You are already friends with this user")
            except Friend.DoesNotExist:
                pass

            raise serializers.ValidationError(
                "You have not sent a friend request to this user")
        return value

    def create(self, validated_data):
        """
        Create a new Friend instance
        """
        return Friend.objects.create(
            user=self.context["request"].user,
            friend=self.user_obj
        )

    def save(self, **kwargs):
        self.friend_request_obj.delete()
        return super().save(**kwargs)


class SendFriendRequestListSerializer(ReadOnlyModelSerializer):
    """
        Serializer for SendFriendRequestList
    """
    to_user = AllUserListSerializer(read_only=True)

    class Meta:
        model = SendFriendRequest
        fields = ("id", "to_user", "created_at")


class FriendListSerializer(ReadOnlyModelSerializer):
    """
        Serializer for FriendList
    """
    friend = AllUserListSerializer()

    class Meta:
        model = Friend
        fields = ("id", "friend", "created_at")
