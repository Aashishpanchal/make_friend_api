from rest_framework import serializers

from post.models import Post
from utility.serializers import ReadOnlyModelSerializer
from numerize.numerize import numerize

from auth_user.api.user_serializers import UserDetailRetrieveSerializer


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ("updated_at", "user")
        read_only_fields = ("id", "created_at",)

        extra_kwargs = {
            "title": {"required": True, "allow_null": False},
            "content": {"required": True, "allow_null": False},
            "post_image": {"required": True, "allow_null": False},
        }

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        post = Post.objects.create(**validated_data)
        return post


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ("created_at", "user")
        read_only_fields = ("id", "updated_at",)

        extra_kwargs = {
            "title": {"required": False, "allow_null": True},
            "content": {"required": False, "allow_null": True},
            "post_image": {"required": False, "allow_null": True},
        }


class PostRetrieveSerializer(ReadOnlyModelSerializer):
    """
        Only Read Data from Post, We cannot change it
    """
    like = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    user = UserDetailRetrieveSerializer(read_only=True)
    post_image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        exclude = ("updated_at",)

    def get_like(self, obj):
        """
        Return the format of number likes of a post
        """
        return numerize(obj.like_count())

    def get_comment(self, obj):
        """
        Return the format of number comments of a post
        """
        return numerize(obj.comment_count())

    def get_post_image(self, obj):
        request = self.context.get('request')
        image_data = {
            'width': obj.post_image.width,
            'height': obj.post_image.height,
            'url': request.build_absolute_uri(obj.post_image.url),
        }
        return image_data


class PostIDSerializer(serializers.Serializer):
    post_id = serializers.UUIDField(required=True, allow_null=False)

    def validate_post_id(self, post_id):
        """
        Check if the post_id is valid
        """
        try:
            self.post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise serializers.ValidationError("Post does not exist")
        return post_id
