from rest_framework.exceptions import ValidationError
from post.api.post_serializers import PostIDSerializer
from post.models import Like


class LikePostSerializer(PostIDSerializer):
    def create(self, validated_data):
        """
        Create a new Like for a Post
        """
        post_id = validated_data.get("post_id")
        try:
            Like.objects.get(user=self.context["request"].user, post=post_id)
            raise ValidationError("You already liked this post")
        except Like.DoesNotExist:
            pass
        user = self.context["request"].user
        like = Like.objects.create(user=user, post=self.post)
        return like
