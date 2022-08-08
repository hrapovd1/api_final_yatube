from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()  # Получаем текущую модель User.


class Group(models.Model):
    """Модель для групп (сообществ)."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    """Модель для постов (записей)."""
    text = models.TextField(
        'Текст поста',
        help_text='Текст нового поста'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        related_name='posts',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
        null=True,
        help_text='Загрузите изображение'
    )

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Модель для комментариев к записям."""
    text = models.TextField(
        'Текст комментария',
        help_text='Текст нового комментария'
    )
    created = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Запись'
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ['-created']


class Follow(models.Model):
    """Модель для подписок на авторов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        unique_together = ['user', 'following']
