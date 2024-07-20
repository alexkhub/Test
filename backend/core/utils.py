from django_filters import rest_framework as filters

from .models import File


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class FileFilter(filters.FilterSet):

    name = CharFilterInFilter(field_name='name', lookup_expr='in')
    date = filters.DateFilter(field_name='date', lookup_expr='gte')
    percentage = filters.RangeFilter()

    class Meta:
        model = File
        fields = ['name', 'date']