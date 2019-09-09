import django_filters
from django.db.models import OuterRef, Subquery
from rest_framework import filters, viewsets
from wagtail.api.v2.filters import OrderingFilter

from api.filters import BoundingBoxFilter, PostgreSQLSearchFilter, \
    DistanceFilter, MemorialFilterSet, AuthorFilterSet
from api.serializers import LanguageSerializer, PeriodSerializer, \
    MemorialTypeSerializer, GenreSerializer, MemorialSerializer, AuthorSerializer, PositionSerializer
from cms.models import LanguageTag, PeriodTag, GenreTag, MemorialTag, Memorial, Author, AuthorName


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        PostgreSQLSearchFilter,
        filters.OrderingFilter,
    )
    filterset_class = AuthorFilterSet

    def get_queryset(self):
        popular_name_qs = AuthorName.objects.filter(author_id=OuterRef('pk')).order_by('sort_order')[:1]
        queryset = Author.objects.annotate(
            academic_title=Subquery(popular_name_qs.values('title')),
            first_name=Subquery(popular_name_qs.values('first_name')),
            last_name=Subquery(popular_name_qs.values('last_name')),
            birth_name=Subquery(popular_name_qs.values('birth_name')),
        ).prefetch_related('names')

        if self.request.user.is_authenticated:
            return queryset
        return queryset.public().live()


class PositionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PositionSerializer
    filter_backends = (
        BoundingBoxFilter,
        DistanceFilter,
    )
    bbox_filter_field = "coordinates"
    distance_filter_field = "coordinates"

    def get_queryset(self):
        queryset = Memorial.objects.all()

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
        queryset = Memorial.objects.select_related('title_image')

        if self.request.user.is_authenticated:
            return queryset
        return queryset.public().live()


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
