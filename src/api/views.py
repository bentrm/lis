"""Read-only API views of the LIS domain."""

from rest_framework import generics, mixins, pagination, versioning

from cms.models import Author, TempLocation

from . import filters, serializers


class DefaultVersioning(versioning.URLPathVersioning):
    """Default versioning scheme of the API."""

    default_version = "v1"
    allowed_versions = ("v1",)
    version_param = "version"


class DefaultResultsetPagination(pagination.PageNumberPagination):
    """Default pagination scheme of the API."""

    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 100


class GenericAPIView(generics.GenericAPIView):
    """Generic view that presets default pagination an versioning classes."""

    pagination_class = DefaultResultsetPagination
    versioning_class = DefaultVersioning


class AuthorList(mixins.ListModelMixin, GenericAPIView):
    """Returns a list of authors."""

    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    filter_class = filters.AuthorFilter
    ordering_fields = ("id", "born", "died", "created")

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

    queryset = TempLocation.objects.all()
    serializer_class = serializers.MemorialSerializer
    filter_class = filters.MemorialFilter
    ordering_fields = ("id",)

    def get(self, *args, **kwargs):
        """Return a list of memorial objects."""
        return self.list(*args, **kwargs)


class MemorialDetail(mixins.RetrieveModelMixin, GenericAPIView):
    """Returns details about a memorial object."""

    queryset = TempLocation.objects.all()
    serializer_class = serializers.MemorialDetailSerializer

    def get(self, *args, **kwargs):
        """Return the memorial object."""
        return self.retrieve(*args, **kwargs)
