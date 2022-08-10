from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для записей."""
    author = serializers.StringRelatedField()
    image = serializers.ImageField(required=False)
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        required=False
    )

    class Meta:
        model = Post
        fields = ('__all__')
        read_only_fields = ('author', 'pub_date')


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для групп записей."""
    class Meta:
        model = Group
        fields = ('__all__')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев к записям."""
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ('__all__')
        read_only_fields = ('author', 'post', 'created')


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок на авторов."""
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )
    user = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'])
        ]

    def validate_following(self, value):
        request = self.context.get('request')
        user = request.user
        if user == value:
            raise serializers.ValidationError("Нельзя подписаться на себя.")
        return value
