import re
import django_filters
from django.db.models import Q
from rest_framework.exceptions import ParseError
from rest_framework_gis.filters import InBBoxFilter, DistanceToPointFilter
from rest_framework_json_api.filters import QueryParameterValidationFilter

from cms.models import Author, Memorial


class BoundingBoxFilter(InBBoxFilter):
    bbox_param = 'spatial[bbox]'


class DistanceFilter(DistanceToPointFilter):
    dist_param = 'spatial[dist]'
    point_param = 'spatial[point]'

    def filter_queryset(self, request, queryset, view):
        print("called")

        filter_field = getattr(view, 'distance_filter_field', None)
        convert_distance_input = getattr(view, 'distance_filter_convert_meters', False)
        geoDjango_filter = 'dwithin'  # use dwithin for points

        if not filter_field:
            return queryset

        point = self.get_filter_point(request)

        print(point)
        if not point:
            return queryset

        # distance in meters
        dist_string = request.query_params.get(self.dist_param, 1000)
        try:
            dist = float(dist_string)
        except ValueError:
            raise ParseError('Invalid distance string supplied for parameter {0}'.format(self.dist_param))

        if convert_distance_input:
            # Warning:  assumes that the point is (lon,lat)
            dist = self.dist_to_deg(dist, point[1])

        return queryset.filter(Q(**{'%s__%s' % (filter_field, geoDjango_filter): (point, dist)}))


class SpatialQueryParameterValidationFilter(QueryParameterValidationFilter):
    query_regex = re.compile(r'^(sort|include)$|^(filter|fields|page|spatial)(\[[\w.\-]+\])?$')


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
