from django.urls import path
from friends.api import friends_apiviews

urlpatterns = [
    path('api/send-friend-request/',
         friends_apiviews.SendFriendRequestAPIView.as_view()),
    path('api/accept-friend-request/',
         friends_apiviews.AcceptFriendRequestAPIView.as_view()),
    path('api/send-friend-request-list/',
         friends_apiviews.SendFriendListAPIView.as_view()),
    path('api/friend-list/', friends_apiviews.FriendListAPIView.as_view()),
    path('api/friend-delete/', friends_apiviews.FriendDeleteAPIView.as_view()),
]
