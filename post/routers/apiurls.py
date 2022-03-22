from django.urls import path

from post.api import post_apiviews
from post.api import like_apiviews
from post.api import comment_apiviews
from post.api import savepost_apiviews

urlpatterns = [
    # POST API Endpoints
    path('api/post_list/', post_apiviews.PostListAPIView.as_view()),
    path('api/post_create/', post_apiviews.PostCreateAPIView.as_view()),
    path('api/post_update/<uuid:pk>/', post_apiviews.PostUpdateAPIView.as_view()),
    path('api/post_retrieve/<uuid:pk>/',
         post_apiviews.PostRetrieveAPIView.as_view()),
    path('api/post_delete/<uuid:pk>/', post_apiviews.PostDeleteAPIView.as_view()),

    # POST Like API Endpoints
    path('api/post_like/', like_apiviews.LikePostAPIView.as_view()),
    path('api/post_dislike/', like_apiviews.DisLikePostAPIView.as_view()),

    # POST Comment API Endpoints
    path('api/post_comment_create/',
         comment_apiviews.PostCommentCreateAPIView.as_view()),
    path('api/post_comment_list/<uuid:post_id>/',
         comment_apiviews.PostCommentListAPIView.as_view()),
    path('api/post_comment_update/<uuid:pk>/',
         comment_apiviews.PostCommentUpdateAPIView.as_view()),
    path('api/post_comment_delete/<uuid:pk>/',
         comment_apiviews.PostCommentDeleteAPIView.as_view()),

    # POST Save API Endpoints
    path('api/post_save/', savepost_apiviews.SavePostView.as_view()),
    path('api/post_unsave/', savepost_apiviews.UnSavePostView.as_view()),
    path('api/post_save_list/', savepost_apiviews.SavePostListView.as_view()),
]
