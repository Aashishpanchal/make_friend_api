from rest_framework.exceptions import ValidationError

from post.api.post_serializers import PostIDSerializer, PostRetrieveSerializer
from post.models import SavePost
from utility.serializers import ReadOnlyModelSerializer


class SavePostSerializer(PostIDSerializer):
    """
    Serializer for save post
    """

    def validate_post_id(self, post_id):
        super().validate_post_id(post_id)
        try:
            SavePost.objects.get(
                user=self.context["request"].user, post__id=post_id)
            raise ValidationError("You already save this post")
        except SavePost.DoesNotExist:
            pass
        return post_id

    def create(self, validated_data):
        """
        Create a new Like for a Post
        """
        user = self.context["request"].user
        like = SavePost.objects.create(user=user, post=self.post)
        return like


class PostRetrieveSerializer(PostRetrieveSerializer):
    """
    Serializer for retrieve post
    """
    user = None

    class Meta(PostRetrieveSerializer.Meta):
        exclude = ("user",)


class SavePostRetrieveSerializer(ReadOnlyModelSerializer):
    post = PostRetrieveSerializer(read_only=True)
    """
    Serializer for save post retrieve
    """
    class Meta:
        model = SavePost
        fields = "__all__"
