from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, pagination, permissions, viewsets
from rest_framework.response import Response
from rest_framework import status

from posts.models import Group, Post, User

from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
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

    def create(self, request):
        following_name = request.data.get('following')
        if (
            not following_name
            or following_name is None
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers)

    def perform_create(self, serializer):
        following_name = self.request.data.get('following')
        following = get_object_or_404(
            User,
            username=following_name
        )
        serializer.save(
            following=following,
            user=self.request.user  # Без этого возникает ошибка:
            # django.db.utils.IntegrityError:
            # NOT NULL constraint failed: posts_follow.user_id
        )
