from rest_framework import mixins
from rest_framework import generics
from rest_framework import pagination
from rest_framework import versioning

from cms.models import pages as models, tags
from . import serializers, filters


class DefaultVersioning(versioning.URLPathVersioning):
    default_version = "v1"
    allowed_versions = ("v1", "v2")
    version_param = "version"


class DefaultResultsetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 100


class GenericAPIView(generics.GenericAPIView):
    pagination_class = DefaultResultsetPagination
    versioning_class = DefaultVersioning


class AuthorList(mixins.ListModelMixin, GenericAPIView):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    filter_class = filters.AuthorFilter
    ordering_fields = ("id", "born", "died", "created")

    def get(self, *args, **kwargs):
        return self.list(*args, **kwargs)


class AuthorDetail(mixins.RetrieveModelMixin, GenericAPIView):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorDetailSerializer

    def get(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)


class MemorialList(mixins.ListModelMixin, GenericAPIView):
    queryset = models.TempLocation.objects.all()
    serializer_class = serializers.MemorialSerializer
    filter_class = filters.MemorialFilter
    ordering_fields = ("id",)

    def get(self, *args, **kwargs):
        return self.list(*args, **kwargs)


class MemorialDetail(mixins.RetrieveModelMixin, GenericAPIView):
    queryset = models.TempLocation.objects.all()
    serializer_class = serializers.MemorialDetailSerializer

    def get(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)
