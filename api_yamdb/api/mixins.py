from rest_framework import filters, mixins, viewsets

from users.permissions import IsAdminOrReadOnly


class AllowedMethodsMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
