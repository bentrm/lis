"""Domain serializers that map CMS pages to JSON representations."""

from rest_framework import serializers
from rest_framework_gis import serializers as geo_serializers
from django.urls import reverse

from cms.models import (
    Author,
    AuthorName,
    GenreTag,
    LanguageTag,
    MemorialTag,
    PeriodTag,
    Memorial,
)

THUMBNAIL_FILTER_SPEC = "fill-300x300|jpegquality-60"
MEDIUM_FILTER_SPEC = "max-1000x1000|jpegquality-60"


class TagSerializer(serializers.ModelSerializer):
    """Abstract serializer class to be used as superclass to all tag serializers."""

    title = serializers.CharField(source="i18n_title")

    class Meta:
        abstract = True
        fields = ("id", "title")


class LanguageTagSerializer(TagSerializer):
    """Language tag serializer handling current user language."""

    class Meta:
        model = LanguageTag
        fields = TagSerializer.Meta.fields


class GenreTagSerializer(TagSerializer):
    """Genre tag serializer handling current user language."""

    class Meta:
        model = GenreTag
        fields = TagSerializer.Meta.fields


class PeriodTagSerializer(TagSerializer):
    """Period tag serializer handling current user language."""

    class Meta:
        model = PeriodTag
        fields = TagSerializer.Meta.fields


class MemorialTagSerializer(TagSerializer):
    """Memorial tag serializer handling current user language."""

    class Meta:
        model = MemorialTag
        fields = TagSerializer.Meta.fields


class SearchResultSerializer(serializers.Serializer):
    """Serializes generic search results to flat JSON objects."""

    title = serializers.CharField(source="i18n_title")
    created = serializers.ReadOnlyField(source="last_published_at")
    thumbnail = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()

    def get_thumbnail(self, obj):
        """Return a static url path to the title images thumbnail rendition."""
        if obj.title_image:
            return obj.title_image.get_rendition(THUMBNAIL_FILTER_SPEC).url

    def get_type(self, obj):
        """Return the model name of the linked content type."""
        return obj.content_type.model

    def get_details(self, obj):
        """Return an API url that offers more details about the object."""
        if isinstance(obj, Author):
            return reverse("api-author-detail", kwargs={"version": "v1", "pk": obj.pk})
        elif isinstance(obj, Memorial):
            return reverse(
                "api-memorial-detail", kwargs={"version": "v1", "pk": obj.pk}
            )


class AuthorNameSerializer(serializers.ModelSerializer):
    """Serializes author names to flat JSON objects."""

    title = serializers.CharField(source="i18n_title")
    first_name = serializers.CharField(source="i18n_first_name")
    last_name = serializers.CharField(source="i18n_last_name")
    birth_name = serializers.CharField(source="i18n_birth_name")
    pseudonym = serializers.BooleanField(source="is_pseudonym")

    class Meta:
        model = AuthorName
        fields = ("title", "first_name", "last_name", "birth_name", "pseudonym")


class AuthorSerializer(serializers.ModelSerializer):
    """Serializes Author pages to flat JSON objects output to list views."""

    name = serializers.ReadOnlyField(source="i18n_title")
    gender = serializers.ReadOnlyField(source="sex")
    thumbnail = serializers.SerializerMethodField()
    languages = LanguageTagSerializer(source="language_tags", many=True, read_only=True)
    genres = GenreTagSerializer(source="genre_tags", many=True, read_only=True)
    periods = PeriodTagSerializer(
        source="literary_period_tags", many=True, read_only=True
    )
    created = serializers.ReadOnlyField(source="last_published_at")

    def get_thumbnail(self, obj):
        """Return a static url path to the title images thumbnail rendition."""
        if obj.title_image:
            return obj.title_image.get_rendition(THUMBNAIL_FILTER_SPEC).url

    class Meta:
        model = Author
        fields = (
            "id",
            "name",
            "gender",
            "thumbnail",
            "born",
            "languages",
            "genres",
            "periods",
            "created",
        )


class AuthorDetailSerializer(AuthorSerializer):
    """Serializes Author pages to flat JSON objects output to detail views."""

    cover = serializers.SerializerMethodField()
    names = AuthorNameSerializer(many=True, read_only=True)

    def get_cover(self, obj):
        """Return a static url path to the title images cover rendition."""
        if obj.title_image:
            return obj.title_image.get_rendition(MEDIUM_FILTER_SPEC).url

    class Meta:
        model = Author
        fields = (
            "id",
            "name",
            "thumbnail",
            "cover",
            "names",
            "born",
            "died",
            "languages",
            "genres",
            "periods",
            "created",
        )


class MemorialSerializer(serializers.ModelSerializer):
    """Serializes Memorial pages to flat JSON objects output to list views."""

    title = serializers.ReadOnlyField(source="i18n_title")
    thumbnail = serializers.SerializerMethodField()
    tags = MemorialTagSerializer(source="memorial_type_tags", many=True, read_only=True)
    authors = serializers.SerializerMethodField()
    geometry = geo_serializers.GeometryField(
        precision=5, source="coordinates", read_only=True
    )
    created = serializers.ReadOnlyField(source="last_published_at")

    def get_thumbnail(self, obj):
        """Return a static url path to the title images thumbnail rendition."""
        if obj.title_image:
            return obj.title_image.get_rendition(THUMBNAIL_FILTER_SPEC).url

    def get_authors(self, obj):
        """Return a list of primary keys of related authors."""
        return [location_author.author.pk for location_author in obj.authors.all()]

    def get_tags(self, obj):
        """Return a list of memorial type tags as string."""
        return [tag.i18n_title for tag in obj.memorial_type_tags.all()]

    def get_coordinates(self, obj):
        """Return memorial coordinates as a list."""
        return list(obj.coordinates.coords)

    class Meta:
        model = Memorial
        fields = ("id", "title", "thumbnail", "tags", "authors", "geometry", "created")


class MemorialDetailSerializer(MemorialSerializer):
    """Serializes Memorial pages to flat JSON objects output to detail views."""

    cover = serializers.SerializerMethodField()
    address = serializers.ReadOnlyField(source="i18n_address")
    desc = serializers.ReadOnlyField(source="i18n_introduction")

    def get_cover(self, obj):
        """Return a static url path to the title images cover rendition."""
        if obj.title_image:
            return obj.title_image.get_rendition(MEDIUM_FILTER_SPEC).url

    class Meta:
        model = Memorial
        fields = (
            "id",
            "title",
            "thumbnail",
            "cover",
            "tags",
            "address",
            "desc",
            "authors",
            "geometry",
            "created",
        )
