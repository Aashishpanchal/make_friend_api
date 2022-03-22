from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView

from post.api.comment_serializers import PostCommentCreateSerializer, PostCommentRetrieveSerializer, PostCommentUpdateSerializer
from post.models import Comment
from post.pagination import CommentPagination


class PostCommentCreateAPIView(CreateAPIView):
    serializer_class = PostCommentCreateSerializer


class PostCommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = PostCommentRetrieveSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        return Comment.objects.filter(post__id=post_id)


class PostCommentUpdateAPIView(UpdateAPIView):
    serializer_class = PostCommentUpdateSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)


class PostCommentDeleteAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    lookup_field = 'pk'

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)
