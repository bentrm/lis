import django_filters
from rest_framework import filters, viewsets
from wagtail.api.v2.endpoints import PagesAPIEndpoint
from wagtail.api.v2.filters import RestrictedChildOfFilter, RestrictedDescendantOfFilter, OrderingFilter

from api.filters import BoundingBoxFilter, CustomWagtailSearchBackend, CustomFieldsFilter, PostgreSQLSearchFilter, \
    DistanceFilter, MemorialFilterSet, AuthorFilterSet
from api.serializers import LanguageSerializer, PeriodSerializer, \
    MemorialTypeSerializer, GenreSerializer, MemorialSerializer, AuthorSerializer
from cms.models import LanguageTag, PeriodTag, GenreTag, MemorialTag, Memorial, Author


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        PostgreSQLSearchFilter,
        filters.OrderingFilter,
    )
    filterset_class = AuthorFilterSet

    def get_queryset(self):
        queryset = Author.objects.all()

        if self.request.user.is_authenticated:
            return queryset
        return queryset.public().live()


class MemorialViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MemorialSerializer
    filter_backends = (
        BoundingBoxFilter,
        DistanceFilter,
        django_filters.rest_framework.DjangoFilterBackend,
        PostgreSQLSearchFilter,
        filters.OrderingFilter,
    )
    bbox_filter_field = "coordinates"
    distance_filter_field = "coordinates"
    filterset_class = MemorialFilterSet

    def get_queryset(self):
        queryset = Memorial.objects.all()

        if self.request.user.is_authenticated:
            return queryset
        return queryset.public().live()


class AuthorApiEndpoint(PagesAPIEndpoint):
    filter_backends = [
        CustomFieldsFilter,
        RestrictedChildOfFilter,
        RestrictedDescendantOfFilter,
        OrderingFilter,
        CustomWagtailSearchBackend
    ]
    name = "authors"

    def get_queryset(self):
        request = self.request

        # Get live pages that are not in a private section
        queryset = Author.objects.public().live()

        # Filter by site
        if request.site:
            queryset = queryset.descendant_of(request.site.root_page, inclusive=True)
        else:
            # No sites configured
            queryset = queryset.none()

        return queryset


class MemorialApiEndpoint(PagesAPIEndpoint):
    filter_backends = [
        BoundingBoxFilter,
        CustomFieldsFilter,
        RestrictedChildOfFilter,
        RestrictedDescendantOfFilter,
        OrderingFilter,
        CustomWagtailSearchBackend
    ]
    known_query_parameters = PagesAPIEndpoint.known_query_parameters.union([
        "bbox",
    ])

    listing_default_fields = PagesAPIEndpoint.listing_default_fields + [
        'title_de',
        'title_cs',
        'coordinates',
    ]
    nested_default_fields = PagesAPIEndpoint.nested_default_fields + [
        'title_de',
        'title_cs',
        'coordinates',
    ]

    name = "memorials"
    bbox_filter_field = "coordinates"

    def get_queryset(self):
        request = self.request

        # Get live pages that are not in a private section
        queryset = Memorial.objects.public().live()

        # Filter by site
        if request.site:
            queryset = queryset.descendant_of(request.site.root_page, inclusive=True)
        else:
            # No sites configured
            queryset = queryset.none()

        return queryset


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [
        OrderingFilter,
    ]
    search_fields = [
        'title',
        'title_de',
        'title_cs',
    ]
    ordering_fields = (
        'title',
        'title_de',
        'title_cs',
    )


class LanguageViewSet(TagViewSet):
    queryset = LanguageTag.objects.all()
    serializer_class = LanguageSerializer


class GenreViewSet(TagViewSet):
    queryset = GenreTag.objects.all()
    serializer_class = GenreSerializer


class PeriodViewSet(TagViewSet):
    queryset = PeriodTag.objects.all()
    serializer_class = PeriodSerializer


class MemorialTypeViewSet(TagViewSet):
    queryset = MemorialTag.objects.all()
    serializer_class = MemorialTypeSerializer
