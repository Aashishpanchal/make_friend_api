from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from post.api.like_serializers import LikePostSerializer
from post.api.post_serializers import PostIDSerializer
from post.models import Like


class LikePostAPIView(CreateAPIView):
    """
        Create a Like for a Post
    """
    serializer_class = LikePostSerializer


class DisLikePostAPIView(DestroyAPIView):
    """
        Delete a Like for a Post
    """
    serializer_class = PostIDSerializer

    def destroy(self, request, *args, **kwargs):
        """
            Delete a Like for a Post
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post_id = serializer.validated_data["post_id"]
        try:
            Like.objects.get(user=request.user, post=post_id).delete()
        except Like.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
