from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from friends.models import Friend, SendFriendRequest
from friends.api.friends_serializers import (
    FriendIDSerializer,
    FriendRequestAcceptSerializer,
    FriendListSerializer,
    SendFriendRequestSerializer,
    SendFriendRequestListSerializer
)
from friends.pagination import FriendsPagination


class SendFriendRequestAPIView(CreateAPIView):
    serializer_class = SendFriendRequestSerializer


class AcceptFriendRequestAPIView(CreateAPIView):
    serializer_class = FriendRequestAcceptSerializer


class SendFriendListAPIView(ListAPIView):
    serializer_class = SendFriendRequestListSerializer
    pagination_class = FriendsPagination

    def get_queryset(self):
        return SendFriendRequest.objects.filter(from_user=self.request.user)


class FriendListAPIView(ListAPIView):
    serializer_class = FriendListSerializer
    pagination_class = FriendsPagination

    def get_queryset(self):
        return Friend.objects.filter(
            user=self.request.user
        )


class ClancalSendFriendRequestAPIView(DestroyAPIView):
    serializer_class = FriendIDSerializer

    def destroy(self, request, *args, **kwargs):
        """
            Delete a SendFriendRequest instance
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


class FriendDeleteAPIView(DestroyAPIView):
    serializer_class = FriendIDSerializer

    def destroy(self, request, *args, **kwargs):
        """
            Delete a User from Friends
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            Friend.objects.get(
                user=request.user, friend=serializer.user_obj).delete()
        except Friend.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
