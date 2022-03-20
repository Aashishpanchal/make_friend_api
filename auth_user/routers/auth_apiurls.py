from django.urls import path
from auth_user.api.auth_apiviews import (
    LoginApiView,
    LoginAuthJWTRefreshApiView,
    BlackListLoginAuthJWTApiView,
    AllBlackLoginListAuthJWTApiView,
    JWTokenVerifyAPIView,
)

app_name = 'auth_api'

urlpatterns = [
    path("api/login/token/", LoginApiView.as_view()),
    path("api/login/token/refresh/", LoginAuthJWTRefreshApiView.as_view()),
    path("api/logout/", BlackListLoginAuthJWTApiView.as_view()),
    path("api/logout/all/", AllBlackLoginListAuthJWTApiView.as_view()),
    path("api/login/token/validate/", JWTokenVerifyAPIView.as_view())
]
