from django.urls import path
from auth_user.api import user_apiviews

app_name = 'user_api'

urlpatterns = [
    path('api/signup/', user_apiviews.UserCreateAPIView.as_view()),
    path('api/update/', user_apiviews.UserDetailUpdateAPIView.as_view()),
    path('api/retrieve/<pk>/', user_apiviews.UserDetailRetrieveAPIView.as_view()),
]
