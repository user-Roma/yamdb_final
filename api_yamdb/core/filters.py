import django_filters as df

from reviews.models import Title


class TitleFilters(df.FilterSet):
    """Filters for /titles."""

    category = df.CharFilter(
        field_name='category__slug', lookup_expr='contains')
    genre = df.CharFilter(
        field_name='genre__slug', lookup_expr='contains')
    name = df.CharFilter(
        field_name='name', lookup_expr='contains')
    year = df.NumberFilter(
        field_name='year')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
