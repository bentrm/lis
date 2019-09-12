import django_filters
from django.db.models import Q
from django.template import loader
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from rest_framework.exceptions import ParseError
from rest_framework.filters import SearchFilter
from rest_framework_gis.filters import InBBoxFilter, DistanceToPointFilter
from wagtail.api.v2.utils import BadRequestError
from wagtail.search.backends import get_search_backend

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


class PostgresSearchFilter(SearchFilter):

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
            queryset = sb.autocomplete(
                search_query,
                queryset,
                operator=search_operator,
                order_by_relevance=order_by_relevance
            )

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


class BoundingBoxFilter(InBBoxFilter):
    bbox_param = 'bbox'


class DistanceFilter(DistanceToPointFilter):
    dist_param = 'dist'
    point_param = 'point'

    def filter_queryset(self, request, queryset, view):
        filter_field = getattr(view, 'distance_filter_field', None)
        convert_distance_input = getattr(view, 'distance_filter_convert_meters', False)
        # noinspection PyPep8Naming
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
