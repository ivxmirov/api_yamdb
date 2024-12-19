from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constsnts import (
    USERNAME,
    EMAIL,
    ROLE,
    FIRST_NAME,
    LAST_NAME,
    USER,
    ADMIN,
    MODERATOR,
    CONFIRMATION_CODE_LENGTH,
    ROLE_CHOICES
)


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=USERNAME,
        unique=True,
        blank=False,
        null=False,
        verbose_name='username'
    )
    email = models.EmailField(
        max_length=EMAIL,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Эл. адрес'
    )
    role = models.CharField(
        max_length=ROLE,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True,
        verbose_name='Пользовательская роль'
    )
    first_name = models.CharField(
        max_length=FIRST_NAME,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=LAST_NAME,
        blank=True,
        verbose_name='Фамилия'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    confirmation_code = models.CharField(
        max_length=CONFIRMATION_CODE_LENGTH,
        null=True,
        blank=False,
        verbose_name='Код подтверждения'
    )

    @property
    def is_admin(self):
        """Является ли пользователь администратором или суперпользователем"""
        return self.role == ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        """Является ли пользователь модератором"""
        return self.role == MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
