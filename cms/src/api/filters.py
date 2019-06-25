import re
import django_filters
from rest_framework_json_api.filters import QueryParameterValidationFilter

from cms.models import Author, Memorial


class SpatialQueryParameterValidationFilter(QueryParameterValidationFilter):
    query_regex = re.compile(r'^(sort|include|in_bbox)$|^(filter|fields|page)(\[[\w\.\-]+\])?$')



class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class AuthorFilter(django_filters.FilterSet):
    languages = NumberInFilter(field_name='language_tags', lookup_expr='in')
    genres = NumberInFilter(field_name='genre_tags', lookup_expr='in')
    periods = NumberInFilter(field_name='litarery_period_tags', lookup_expr='in')

    class Meta:
        model = Author
        fields = {
            'sex': ('exact',),
            'date_of_birth_year': ('exact', 'lt', 'gt', 'gte', 'lte', 'in'),
            'date_of_birth_month': ('exact', 'lt', 'gt', 'gte', 'lte', 'in'),
            'date_of_birth_day': ('exact', 'lt', 'gt', 'gte', 'lte', 'in'),
            'date_of_death_year': ('exact', 'lt', 'gt', 'gte', 'lte', 'in'),
            'date_of_death_month': ('exact', 'lt', 'gt', 'gte', 'lte', 'in'),
            'date_of_death_day': ('exact', 'lt', 'gt', 'gte', 'lte', 'in'),
        }


class MemorialFilter(django_filters.FilterSet):
    memorial_types = NumberInFilter(field_name='memorial_type_tags', lookup_expr='in')
    authors = NumberInFilter(field_name='remembered_authors', lookup_expr='in')

    class Meta:
        model = Memorial
        fields = {}
