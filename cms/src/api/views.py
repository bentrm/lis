import django_filters
from django.db.models import OuterRef, Subquery, Prefetch
from rest_framework import filters, viewsets
from wagtail.api.v2.filters import OrderingFilter

from api.filters import BoundingBoxFilter, PostgresSearchFilter, \
    DistanceFilter, MemorialFilterSet, AuthorFilterSet
from api.serializers import LanguageSerializer, PeriodSerializer, \
    MemorialTypeSerializer, GenreSerializer, MemorialDetailSerializer, AuthorDetailSerializer, PositionSerializer, \
    AuthorListSerializer, MemorialListSerializer
from cms.models import LanguageTag, PeriodTag, GenreTag, MemorialTag, Memorial, Author, AuthorName


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    filterset_class = AuthorFilterSet
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        PostgresSearchFilter,
        filters.OrderingFilter,
    )
    serializer_class = AuthorDetailSerializer
    serializer_action_classes = {
        'list': AuthorListSerializer,
    }

    def get_queryset(self):
        popular_name_qs = AuthorName.objects.filter(author_id=OuterRef('pk')).order_by('sort_order')[:1]
        queryset = Author.objects.annotate(
            academic_title=Subquery(popular_name_qs.values('title')),
            first_name=Subquery(popular_name_qs.values('first_name')),
            last_name=Subquery(popular_name_qs.values('last_name')),
            birth_name=Subquery(popular_name_qs.values('birth_name')),
        )

        queryset = queryset.select_related('title_image')

        if self.action == 'list':
            # an author may be known by multiple names
            queryset = queryset.prefetch_related('names')

            # related memorials might not be published
            memorials_qs = Memorial.objects.public().live()
            memorials_prefetch = Prefetch('memorials', queryset=memorials_qs)
            queryset = queryset.prefetch_related(memorials_prefetch)

        return queryset.public().live()

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except KeyError:
            return super().get_serializer_class()


class PositionViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (
        BoundingBoxFilter,
        DistanceFilter,
    )
    bbox_filter_field = 'coordinates'
    distance_filter_field = 'coordinates'
    serializer_class = PositionSerializer

    def get_queryset(self):
        return Memorial.objects.public().live()


class MemorialViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (
        BoundingBoxFilter,
        DistanceFilter,
        django_filters.rest_framework.DjangoFilterBackend,
        PostgresSearchFilter,
        filters.OrderingFilter,
    )
    filterset_class = MemorialFilterSet
    bbox_filter_field = 'coordinates'
    distance_filter_field = 'coordinates'
    serializer_class = MemorialDetailSerializer
    serializer_action_classes = {
        'list': MemorialListSerializer,
    }

    def get_queryset(self):
        queryset = Memorial.objects.select_related('title_image')
        return queryset.public().live()

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except KeyError:
            return super().get_serializer_class()


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
