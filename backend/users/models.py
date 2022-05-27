from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Почта',
        max_length=254,
        unique=True)
    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        unique=True)
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150)
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                name='unique_subscription',
                fields=['user', 'author'],
            )
        ]

    def __str__(self):
        return (f'Подписчик: { self.user.username }\n'
                f'Автор: { self.author.username }')
