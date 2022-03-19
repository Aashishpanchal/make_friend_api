from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.utils import aware_utcnow

from rest_framework import exceptions, serializers

from django.contrib.auth.models import update_last_login
from django.contrib.auth import get_user_model, authenticate

from auth_user.constants import Messages


# get User model
UserModel = get_user_model()


class ExpiredTokenMix:
    def Expiredhandle(self):
        OutstandingToken.objects.filter(
            expires_at__lte=aware_utcnow()).delete()


class AuthUserSerializer(TokenObtainSerializer):
    default_error_messages = {
        'no_active_account': Messages.NO_ACTIVE_ACCOUNT,
        'no_user_found': Messages.NO_USER_FOUND,
        'incorrect_password': Messages.INCORRECT_PASSWORD
    }

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        self.user = self._getUser(username, password)

        self.user = authenticate(request=self.context.get(
            'request'), username=self.user.username, password=password)
        return {}

    def _getUser(self, username, password):
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_user_found'],
                'no_user_found'
            )
        else:
            if not user.check_password(password):
                raise exceptions.AuthenticationFailed(
                    self.error_messages['incorrect_password'],
                    'incorrect_password'
                )
            else:
                if not self._user_can_authenticate(user):
                    raise exceptions.AuthenticationFailed(
                        self.error_messages['no_active_account'],
                        'no_active_account'
                    )
        return user

    def _user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None


class AuthJWTSerializer(AuthUserSerializer, ExpiredTokenMix):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class TokenField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['required'] = True
        kwargs['write_only'] = True

        super().__init__(*args, **kwargs)


class BlacklistRefreshSerializer(serializers.Serializer):
    refresh = TokenField()
    default_error_messages = {
        'bad_token': Messages.BAD_TOKEN
    }

    def validate(self, attrs):
        self.refreshToken = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.refreshToken).blacklist()
        except TokenError:
            raise InvalidToken(
                self.error_messages['bad_token'], code='token_not_valid')
