import datetime

from django.db import models

from rest_framework import serializers, validators

from reviews.models import Category, Genre, Title, Review, Comment
from reviews.constants import SLUG


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=SLUG,
        validators=[
            validators.UniqueValidator(
                queryset=Category.objects.all(),
                message='Объект с таким slug уже существует.'
            )
        ]
    )

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=SLUG,
        validators=[
            validators.UniqueValidator(
                queryset=Genre.objects.all(),
                message='Объект с таким slug уже существует.'
            )
        ]
    )

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = serializers.SlugRelatedField(
        many=True,
        allow_null=True,
        allow_empty=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        read_only_fields = ('id', 'rating',)

    def to_representation(self, instance):
        serializer = TitleSerializerSafe(instance)
        return serializer.data

    def validate_year(self, value):
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError("Укажите реальный год.")
        return value

    def get_rating(self, obj):
        average = obj.reviews.all().aggregate(
            models.Avg('score')
        ).get('score__avg')
        return average


class TitleSerializerSafe(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(
        many=True,
        read_only=True
    )
    category = CategorySerializer(
        read_only=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        read_only_fields = ('rating',)

    def get_rating(self, obj):
        average = obj.reviews.all().aggregate(
            models.Avg('score')
        ).get('score__avg')
        return average


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('author',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('author',)
