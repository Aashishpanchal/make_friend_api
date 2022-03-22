from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status

from post.api.savepost_serializers import SavePostSerializer, SavePostRetrieveSerializer
from post.api.post_serializers import PostIDSerializer
from post.models import SavePost
from post.pagination import SavePostPagination


class SavePostView(CreateAPIView):
    """
        Create a Like for a Post
    """
    serializer_class = SavePostSerializer


class UnSavePostView(DestroyAPIView):
    """
        Delete a Like for a SavePost
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
            SavePost.objects.get(user=request.user, post=post_id).delete()
        except SavePost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)


class SavePostListView(ListAPIView):
    """
        List all SavePost
    """
    serializer_class = SavePostRetrieveSerializer
    pagination_class = SavePostPagination

    def get_queryset(self):
        """
            Return all SavePost for a user
        """
        return SavePost.objects.filter(user=self.request.user)
