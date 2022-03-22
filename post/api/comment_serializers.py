from rest_framework import serializers
from utility.serializers import ReadOnlyModelSerializer

from post.models import Comment, Post


class PostCommentCreateSerializer(serializers.ModelSerializer):
    post_id = serializers.UUIDField(required=True, allow_null=False)

    class Meta:
        model = Comment
        exclude = ("updated_at", "user", "post")
        read_only_fields = ("id", "created_at",)

        extra_kwargs = {
            "content": {"required": True, "allow_null": False},
        }

    def validate_post_id(self, value):
        try:
            Post.objects.get(id=value)
        except Post.DoesNotExist:
            raise serializers.ValidationError("post id does not exist")
        try:
            Comment.objects.get(
                post__id=value, user=self.context["request"].user)
            raise serializers.ValidationError(
                "You already commented this post")
        except Comment.DoesNotExist:
            pass
        return value

    def create(self, validated_data):
        post = Post.objects.get(id=validated_data["post_id"])
        comment = Comment.objects.create(
            post=post,
            user=self.context["request"].user,
            content=validated_data["content"]
        )
        return comment


class PostCommentRetrieveSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Comment
        exclude = ("updated_at", )
        read_only_fields = ("id", "created_at",)


class PostCommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ("updated_at", "user", "post")
        read_only_fields = ("id", "created_at",)

        extra_kwargs = {
            "content": {"required": False, "allow_null": True},
        }
