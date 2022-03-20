from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from auth_user.models import User
from auth_user.api.user_serializers import (
    UserCreatePasswordRetypeSerializer, UserDetailUpdateSerializer, UserDetailRetrieveSerializer)


class UserCreateAPIView(CreateAPIView):
    """
        Create a new user.
    """
    serializer_class = UserCreatePasswordRetypeSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # its a method of CreateAPIView, is save serializer.data in database
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserDetailUpdateAPIView(UpdateAPIView):
    """
        update user's profile information
    """
    serializer_class = UserDetailUpdateSerializer
    # by default, permission_classes isAuthenticated

    def get_queryset(self):
        return User.objects.get(pk=self.request.user.pk)

    def update(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(
            instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class UserDetailRetrieveAPIView(RetrieveAPIView):
    """
    Retrieve user's profile information
    """
    permission_classes = (AllowAny,)
    serializer_class = UserDetailRetrieveSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'
