import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name='category__slug', lookup_expr='icontains'
    )
    genre = django_filters.CharFilter(
        field_name='genre__slug', lookup_expr='icontains'
    )
    name = django_filters.CharFilter(lookup_expr='icontains')
    filter = django_filters.NumberFilter(lookup_expr='iexect')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
