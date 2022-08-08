from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    CommentDetail,
    CommentList,
    FollowViewSet,
    GroupViewSet,
    PostViewSet
)


router = SimpleRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register('follow', FollowViewSet, basename='follow')


urlpatterns = [
    path(
        'v1/posts/<int:post_id>/comments/<int:comment_id>/',
        CommentDetail.as_view()
    ),
    path('v1/posts/<int:post_id>/comments/', CommentList.as_view()),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router.urls))
]
