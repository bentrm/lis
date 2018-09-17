"""Read-only API views of the LIS domain."""

from django.contrib.contenttypes.models import ContentType
from rest_framework import (
    generics,
    mixins,
    pagination,
    versioning,
    filters as drf_filters,
)
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework_gis.filters import InBBoxFilter, TMSTileFilter

from cms.models import I18nPage, Author, Memorial

from . import filters, serializers


class DefaultVersioning(versioning.URLPathVersioning):
    """Default versioning scheme of the API."""

    default_version = "v1"
    allowed_versions = ("v1",)


class DefaultResultsetPagination(pagination.PageNumberPagination):
    """Default pagination scheme of the API."""

    page_size = 10
    page_size_query_param = "size"
    max_page_size = 25


class GenericAPIView(generics.GenericAPIView):
    """Generic view that presets default pagination an versioning classes."""

    pagination_class = DefaultResultsetPagination
    versioning_class = DefaultVersioning


class SearchView(mixins.ListModelMixin, GenericAPIView):
    """Returns a list of found objects."""

    serializer_class = serializers.SearchResultSerializer
    filter_backends = (
        DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
    )
    filter_class = filters.SearchResultFilter
    search_fields = ("title", "title_de", "title_cs")
    ordering_fields = ("id", "title")

    def get_queryset(self):
        """Return a generic page queryset."""
        return I18nPage.objects.filter(
            content_type__in=self.get_content_types()
        ).specific()

    def get(self, *args, **kwargs):
        """Return a list of search results."""
        return self.list(*args, **kwargs)

    def get_content_types(self):
        return ContentType.objects.filter(
            app_label="cms", model__in=["author", "memorial"]
        )


class AuthorList(mixins.ListModelMixin, GenericAPIView):
    """Returns a list of all authors."""

    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    filter_backends = (
        DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
    )
    filter_class = filters.AuthorFilter
    search_fields = ("title", "title_de", "title_cs")
    ordering_fields = ("id", "title")

    def get(self, *args, **kwargs):
        """Return a list of author objects."""
        return self.list(*args, **kwargs)


class AuthorDetail(mixins.RetrieveModelMixin, GenericAPIView):
    """Returns details about an author."""

    queryset = Author.objects.all()
    serializer_class = serializers.AuthorDetailSerializer

    def get(self, *args, **kwargs):
        """Return the author object."""
        return self.retrieve(*args, **kwargs)


class MemorialList(mixins.ListModelMixin, GenericAPIView):
    """Returns a list of memorials."""

    queryset = Memorial.objects.all()
    serializer_class = serializers.MemorialSerializer
    filter_class = filters.MemorialFilter
    filter_backends = (
        InBBoxFilter,
        TMSTileFilter,
        DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
    )
    bbox_filter_field = "coordinates"
    bbox_filter_include_overlapping = True
    search_fields = ("title", "title_de", "title_cs")
    ordering_fields = ("id", "title")

    def get(self, *args, **kwargs):
        """Return a list of memorial objects."""
        return self.list(*args, **kwargs)


class MemorialDetail(mixins.RetrieveModelMixin, GenericAPIView):
    """Returns details about a memorial object."""

    queryset = Memorial.objects.all()
    serializer_class = serializers.MemorialDetailSerializer

    def get(self, *args, **kwargs):
        """Return the memorial object."""
        return self.retrieve(*args, **kwargs)
