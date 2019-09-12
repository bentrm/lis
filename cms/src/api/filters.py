import django_filters
from django.utils.translation import gettext as _
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.template import loader
from django.utils.translation import get_language
from rest_framework.exceptions import ParseError
from rest_framework.filters import BaseFilterBackend, SearchFilter
from rest_framework_gis.filters import InBBoxFilter, DistanceToPointFilter
from taggit.managers import TaggableManager
from wagtail.api.v2.filters import FieldsFilter
from wagtail.api.v2.utils import BadRequestError, parse_boolean
from wagtail.search.backends import get_search_backend
from wagtail.search.backends.base import FilterFieldError, OrderByFieldError

from cms.models import Author, Memorial, GenreTag, LanguageTag, PeriodTag, MemorialTag

GENDER_CHOICES = (
    ('F', _('Female')),
    ('M', _('Male')),
)


class AuthorFilterSet(django_filters.FilterSet):
    gender = django_filters.ChoiceFilter(
        label=_('Gender'),
        field_name='sex',
        choices=GENDER_CHOICES
    )
    genre = django_filters.ModelMultipleChoiceFilter(
        label=_('Genre'),
        field_name='genre_tags',
        queryset=GenreTag.objects.all()
    )
    language = django_filters.ModelMultipleChoiceFilter(
        label=_('Language'),
        field_name='language_tags',
        queryset=LanguageTag.objects.all()
    )
    period = django_filters.ModelMultipleChoiceFilter(
        label=_('Period'),
        field_name='literary_period_tags',
        queryset=PeriodTag.objects.all()
    )

    class Meta:
        model = Author
        fields = ('gender', 'genre', 'language', 'period')


class MemorialFilterSet(django_filters.FilterSet):
    author = django_filters.ModelMultipleChoiceFilter(
        label=_('Author'),
        field_name='remembered_authors',
        queryset=Author.objects.live().public()
    )
    memorial_type = django_filters.ModelMultipleChoiceFilter(
        label=_('Memorial type'),
        field_name='memorial_type_tags',
        queryset=MemorialTag.objects.all()
    )

    class Meta:
        model = Memorial
        fields = ('author', 'memorial_type',)


class PostgreSQLSearchFilter(SearchFilter):

    def filter_queryset(self, request, queryset, view):
        if 'search' in request.GET:

            search_query = request.GET['search']
            search_operator = request.GET.get('search_operator', None)
            order_by_relevance = 'ordering' not in request.GET

            language_code = get_language()
            if language_code == 'en':
                search_backend = 'default'
            elif language_code == 'de':
                search_backend = 'german'
            elif language_code == 'cs':
                search_backend = 'default'
            else:
                raise BadRequestError("Unsupported language for searching: " + str(language_code))

            sb = get_search_backend(search_backend)
            queryset = sb.autocomplete(search_query, queryset, operator=search_operator, order_by_relevance=order_by_relevance)

        return queryset

    def to_html(self, request, queryset, view):
        term = self.get_search_terms(request)
        term = term[0] if term else ''
        context = {
            'param': self.search_param,
            'term': term
        }
        template = loader.get_template(self.template)
        return template.render(context)


class CustomWagtailSearchBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        """
        This performs a full-text search on the result set
        Eg: ?search=James Joyce
        """
        search_enabled = getattr(settings, 'WAGTAILAPI_SEARCH_ENABLED', True)

        if 'search' in request.GET:
            if not search_enabled:
                raise BadRequestError("search is disabled")

            print(getattr(queryset, '_filtered_by_tag', False))

            # Searching and filtering by tag at the same time is not supported
            if getattr(queryset, '_filtered_by_tag', False):
                raise BadRequestError("filtering by tag with a search query is not supported")

            search_query = request.GET['search']
            search_operator = request.GET.get('search_operator', None)
            order_by_relevance = 'order' not in request.GET

            language_code = get_language()
            if language_code == 'en':
                search_backend = 'default'
            elif language_code == 'de':
                search_backend = 'german'
            elif language_code == 'cs':
                search_backend = 'default'
            else:
                raise BadRequestError("Unsupported language for searching: " + str(language_code))

            sb = get_search_backend(search_backend)
            try:
                queryset = sb.autocomplete(search_query, queryset, operator=search_operator, order_by_relevance=order_by_relevance)
            except FilterFieldError as e:
                print(e)
                raise BadRequestError("cannot filter by '{}' while searching (field is not indexed)".format(e.field_name))
            except OrderByFieldError as e:
                raise BadRequestError("cannot order by '{}' while searching (field is not indexed)".format(e.field_name))

        return queryset


class BoundingBoxFilter(InBBoxFilter):
    bbox_param = 'bbox'


class DistanceFilter(DistanceToPointFilter):
    dist_param = 'dist'
    point_param = 'point'

    def filter_queryset(self, request, queryset, view):
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


class CustomFieldsFilter(FieldsFilter):
    def filter_queryset(self, request, queryset, view):
        """
        This performs field level filtering on the result set
        Eg: ?title=James Joyce
        """
        fields = set(view.get_available_fields(queryset.model, db_fields_only=True))

        for field_name, values in request.GET.lists():
            if field_name in fields:
                try:
                    field = queryset.model._meta.get_field(field_name)
                except LookupError:
                    field = None

                # Convert value into python
                for value in values:
                    try:
                        if isinstance(field, (models.BooleanField, models.NullBooleanField)):
                            value = parse_boolean(value)
                        elif isinstance(field, (models.IntegerField, models.AutoField)):
                            value = int(value)
                    except ValueError as e:
                        raise BadRequestError("field filter error. '%s' is not a valid value for %s (%s)" % (
                            value,
                            field_name,
                            str(e)
                        ))

                    if isinstance(field, TaggableManager):
                        for tag in value.split(','):
                            queryset = queryset.filter(**{field_name + '__name': tag})

                        # Stick a message on the queryset to indicate that tag filtering has been performed
                        # This will let the do_search method know that it must raise an error as searching
                        # and tag filtering at the same time is not supported
                        queryset._filtered_by_tag = True
                    else:
                        queryset = queryset.filter(**{field_name: value})

        return queryset
