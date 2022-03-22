from django.urls import path

from follow.api import follow_apiviews

urlpatterns = [
    path('api/follow_now/', follow_apiviews.FollowNowAPIView.as_view()),
    path('api/unfollow_now/', follow_apiviews.UnFollowNowAPIView.as_view()),
    path('api/follows_list/', follow_apiviews.FollowListAPIView.as_view()),
]
