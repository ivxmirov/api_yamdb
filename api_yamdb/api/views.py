from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers

from api.filters import TitleFilter
from api.mixins import AllowedMethodsMixin
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleSerializerSafe,
    ReviewSerializer,
    CommentSerializer,
)
from reviews.models import Category, Genre, Title, Review, Comment
from users.permissions import IsAdminOrModeratorOrAuthor, IsAdminOrReadOnly


class GenreViewSet(AllowedMethodsMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(AllowedMethodsMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializerSafe
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrModeratorOrAuthor,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title=title_id)

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user, title=self.get_title())
        except IntegrityError:
            raise serializers.ValidationError('Not unique!',)


class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrModeratorOrAuthor,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review=review_id)

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
