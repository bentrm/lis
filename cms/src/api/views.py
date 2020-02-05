import django_filters
from django.db.models import OuterRef, Subquery, Prefetch, Count, Q
from django.http import Http404
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.filters import BoundingBoxFilter, PostgresSearchFilter, \
    DistanceFilter, MemorialFilterSet, AuthorFilterSet
from api.serializers import LanguageSerializer, PeriodSerializer, \
    MemorialTypeSerializer, GenreSerializer, MemorialDetailSerializer, AuthorDetailSerializer, \
    AuthorListSerializer, MemorialListSerializer, MemorialPathDetailSerializer, \
    MemorialPathListSerializer, \
    Level1Serializer, Level2Serializer, Level3Serializer
from cms.models import LanguageTag, PeriodTag, GenreTag, MemorialTag, Memorial, Author, AuthorName, \
    MemorialPath, \
    Level1Page, Level2Page, Level3Page
# Notice: All views in this page override the get_queryset method to make sure the language code
#         is set appropriately. Otherwise the queryset will be prepared before any language
#         information is available to the custom translation processor.
from cms.models.base import BlogPage


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


class BlogPageViewSet(ActionAwareReadOnlyModelViewSet):
    lookup_field = 'slug'

    def get_queryset(self):
        return BlogPage.objects.live().public()

    def get_serializer_class(self):
        if self.action == 'list':
            from api.serializers import BlogPageSerializer
            return BlogPageSerializer
        else:
            from api.serializers import BlogPageDetailSerializer
            return BlogPageDetailSerializer


class AuthorViewSet(ActionAwareReadOnlyModelViewSet):
    lookup_field = 'slug'
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

    @action(detail=True)
    def discover(self, request, slug=None):
        try:
            page = Level1Page.objects.child_of(Author.objects.get(slug=slug)).get()
        except (Level1Page.DoesNotExist, Author.DoesNotExist):
            raise Http404

        serializer = Level1Serializer(instance=page)
        return Response(serializer.data)

    @action(detail=True)
    def research(self, request, slug=None):
        try:
            page = Level2Page.objects.child_of(Author.objects.get(slug=slug)).get()
        except (Level2Page.DoesNotExist, Author.DoesNotExist):
            raise Http404

        serializer = Level2Serializer(instance=page)
        return Response(serializer.data)

    @action(detail=True)
    def material(self, request, slug=None):
        try:
            page = Level3Page.objects.child_of(Author.objects.get(slug=slug)).get()
        except (Level3Page.DoesNotExist, Author.DoesNotExist):
            raise Http404

        serializer = Level3Serializer(instance=page)
        return Response(serializer.data)


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
