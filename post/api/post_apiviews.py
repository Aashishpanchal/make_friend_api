from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView

from post.models import Post
from post.api.post_serializers import PostRetrieveSerializer, PostCreateSerializer, PostUpdateSerializer
from post.pagination import PostPagination


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostRetrieveSerializer
    pagination_class = PostPagination
    # by default, permission_classes isAuthenticated


class PostCreateAPIView(CreateAPIView):
    serializer_class = PostCreateSerializer
    # by default, permission_classes isAuthenticated


class PostUpdateAPIView(UpdateAPIView):
    serializer_class = PostUpdateSerializer
    # by default, permission_classes isAuthenticated

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post
    serializer_class = PostRetrieveSerializer
    # by default, permission_classes isAuthenticated


class PostDeleteAPIView(DestroyAPIView):
    serializer_class = PostRetrieveSerializer
    # by default, permission_classes isAuthenticated

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)
