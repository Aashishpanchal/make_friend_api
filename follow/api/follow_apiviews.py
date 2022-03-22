from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from follow.api.follow_serializers import FollowRetrieveSerializer, FollowIDSerializer, FollowNowSerializer
from follow.pagination import FollowsPagination

from follow.models import Follow


class FollowNowAPIView(CreateAPIView):
    """
        Create a Follow for a User
    """
    serializer_class = FollowNowSerializer


class UnFollowNowAPIView(DestroyAPIView):
    serializer_class = FollowIDSerializer

    def destroy(self, request, *args, **kwargs):
        """
            Delete a User from Follow
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            Follow.objects.get(
                user=request.user, followed=serializer.followed_user_obj).delete()
        except Follow.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowListAPIView(ListAPIView):
    """
        List all Follows
    """
    serializer_class = FollowRetrieveSerializer
    pagination_class = FollowsPagination

    def get_queryset(self):
        return self.request.user.follow_follower.all()
