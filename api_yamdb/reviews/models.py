from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

from reviews.constants import (
    MIN_RATE,
    MAX_RATE,
    NAME,
    SLUG,
    DESCRIPTION,
    COMMENT_PREVIEW
)

User = get_user_model()


class Category(models.Model):

    name = models.CharField(max_length=NAME, verbose_name='Название')
    slug = models.SlugField(max_length=SLUG, verbose_name='Идентификатор')

    class Meta:
        ordering = ('name',)
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):

    name = models.CharField(max_length=NAME, verbose_name='Название')
    slug = models.SlugField(max_length=SLUG, verbose_name='Идентификатор')

    class Meta:
        ordering = ('name',)
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):

    name = models.CharField(max_length=NAME, verbose_name='Название')
    year = models.IntegerField(verbose_name='Год')
    rating = models.IntegerField(
        blank=False,
        null=True,
        verbose_name='Рейтинг'
    )
    description = models.CharField(
        max_length=DESCRIPTION,
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(Genre, verbose_name='Жанры')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор публикации'
    )
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                MIN_RATE,
                message=f'Оценка не может быть ниже {MIN_RATE}!',
            ),
            MaxValueValidator(
                MAX_RATE,
                message=f'Оценка не может быть ниже {MAX_RATE}!',
            ),
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review_per_title_for_user'
            )
        ]
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return (
            f'Привет, {self.author}!'
            f'\nВы оставили отзыв на произведение {self.title}.'
        )


class Comment(models.Model):

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор публикации'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:COMMENT_PREVIEW]
