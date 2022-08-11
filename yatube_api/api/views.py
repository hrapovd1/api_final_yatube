from posts.models import Group, Post
from rest_framework import filters, generics, pagination, permissions, viewsets

from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для записей."""
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
        & IsOwnerOrReadOnly
    ]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для групп записей."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentList(generics.ListCreateAPIView):
    """View класс для списка комментариев."""
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = Post.objects.get(
            id=self.kwargs['post_id']
        )
        comments = post.comments
        return comments

    def perform_create(self, serializer):
        post = Post.objects.get(
            id=self.kwargs['post_id']
        )
        serializer.save(
            author=self.request.user,
            post=post
        )


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """View класс для комментария."""
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
        & IsOwnerOrReadOnly
    ]
    serializer_class = CommentSerializer
    lookup_field = 'post_id'

    def get_queryset(self, **kwargs):
        post = Post.objects.get(
            id=self.kwargs['post_id']
        )
        comment = post.comments.filter(
            id=self.kwargs['comment_id']
        )
        return comment


class FollowViewSet(viewsets.ModelViewSet):
    """ViewSet для подписок на авторов."""
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
    permission_classes = [
        permissions.IsAuthenticated
        & IsOwnerOrReadOnly
    ]

    def get_queryset(self):
        user = self.request.user
        return user.follower

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user  # Без этого возникает ошибка:
            # django.db.utils.IntegrityError:
            # NOT NULL constraint failed: posts_follow.user_id
        )
