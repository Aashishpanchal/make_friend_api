from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import(
    TokenRefreshSerializer as AuthJWTRefreshSerializer,
    TokenVerifySerializer,
)

from auth_user.api.auth_serializers import (
    AuthJWTSerializer,
    BlacklistRefreshSerializer,
)


class LoginApiView(TokenViewBase):
    http_method_names = ['post']
    serializer_class = AuthJWTSerializer
    permission_classes = (AllowAny,)


class LoginAuthJWTRefreshApiView(TokenViewBase):
    http_method_names = ['post']
    serializer_class = AuthJWTRefreshSerializer
    permission_classes = (AllowAny,)


class BlackListLoginAuthJWTApiView(GenericAPIView):
    http_method_names = ['post']
    permission_classes = (IsAuthenticated, )
    serializer_class = BlacklistRefreshSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={
            'token_block': True
        }, status=status.HTTP_200_OK)


class AllBlackLoginListAuthJWTApiView(APIView):
    """"All Token Add in BlackList database"""
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        total_block_token = 0
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)
            if _:
                total_block_token += 1
        context = {
            'detail': 'all token blocked',
            'total_token': len(tokens),
            'total_block_token': (len(tokens) - total_block_token),
            'current_block_token': total_block_token
        }
        return Response(context, status=status.HTTP_205_RESET_CONTENT)


class JWTokenVerifyAPIView(TokenViewBase):
    permission_classes = (AllowAny,)
    serializer_class = TokenVerifySerializer
