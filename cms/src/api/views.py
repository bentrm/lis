import django_filters
from django.db.models import OuterRef, Subquery, Prefetch, Count, Q, F, When, Case
from django.utils.translation import get_language
from rest_framework import filters, viewsets

from api.filters import BoundingBoxFilter, PostgresSearchFilter, \
    DistanceFilter, MemorialFilterSet, AuthorFilterSet
from api.serializers import LanguageSerializer, PeriodSerializer, \
    MemorialTypeSerializer, GenreSerializer, MemorialDetailSerializer, AuthorDetailSerializer, \
    AuthorListSerializer, MemorialListSerializer, MemorialPathDetailSerializer, MemorialPathListSerializer
from cms.models import LanguageTag, PeriodTag, GenreTag, MemorialTag, Memorial, Author, AuthorName, MemorialPath


# Notice: All views in this page override the get_queryset method to make sure the language code
#         is set appropriately. Otherwise the querset will be prepared before any language
#         information is available to the custom translation processor.


class ActionAwareReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    list_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'list':
            assert self.list_serializer_class is not None, (
                "'%s' should either include a `list_serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
            )
            return self.list_serializer_class
        else:
            return super().get_serializer_class()


class AuthorViewSet(ActionAwareReadOnlyModelViewSet):
    filterset_class = AuthorFilterSet
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        PostgresSearchFilter,
        filters.OrderingFilter,
    )
    serializer_class = AuthorDetailSerializer
    list_serializer_class = AuthorListSerializer

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


class MemorialViewSet(ActionAwareReadOnlyModelViewSet):
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
    list_serializer_class = MemorialListSerializer

    def get_queryset(self):
        """Overrides default to make sure language is set when processing the view."""
        return Memorial.objects.select_related('title_image').public().live()


class MemorialPathViewSet(ActionAwareReadOnlyModelViewSet):
    serializer_class = MemorialPathDetailSerializer
    list_serializer_class = MemorialPathListSerializer

    def get_queryset(self):
        """Overrides default to make sure language is set when processing the view."""
        return MemorialPath.objects.public().live()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [
        filters.OrderingFilter,
    ]


class LanguageViewSet(TagViewSet):
    serializer_class = LanguageSerializer

    def get_queryset(self):
        return LanguageTag.objects.annotate(
            rel_count=Count('authors', filter=Q(authors__live=True))
        ).filter(rel_count__gt=0)


class GenreViewSet(TagViewSet):
    serializer_class = GenreSerializer

    def get_queryset(self):
        return GenreTag.objects.annotate(
            rel_count=Count('authors', filter=Q(authors__live=True))
        ).filter(rel_count__gt=0)


class PeriodViewSet(TagViewSet):
    serializer_class = PeriodSerializer

    def get_queryset(self):
        return PeriodTag.objects.annotate(
            rel_count=Count('authors', filter=Q(authors__live=True))
        ).filter(rel_count__gt=0)


class MemorialTypeViewSet(TagViewSet):
    serializer_class = MemorialTypeSerializer

    def get_queryset(self):
        return MemorialTag.objects.annotate(
            rel_count=Count('memorial_site', filter=Q(memorial_site__live=True))
        ).filter(rel_count__gt=0)
