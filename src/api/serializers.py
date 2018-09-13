"""Domain serializers that map CMS pages to JSON representations."""

from rest_framework import serializers

from cms.models import AuthorName, Author, TempLocation

THUMBNAIL_FILTER_SPEC = "fill-300x300|jpegquality-60"
MEDIUM_FILTER_SPEC = "max-1000x1000|jpegquality-60"


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
    created = serializers.ReadOnlyField(source="last_published_at")

    def get_thumbnail(self, obj):
        """Return a static url path to the title images thumbnail rendition."""
        if obj.title_image:
            return obj.title_image.get_rendition(THUMBNAIL_FILTER_SPEC).url

    class Meta:
        model = Author
        fields = ("id", "name", "gender", "thumbnail", "born", "created")


class AuthorDetailSerializer(AuthorSerializer):
    """Serializes Author pages to flat JSON objects output to detail views."""

    cover = serializers.SerializerMethodField()
    names = AuthorNameSerializer(many=True, read_only=True)
    languages = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    periods = serializers.SerializerMethodField()

    def get_cover(self, obj):
        """Return a static url path to the title images cover rendition."""
        if obj.title_image:
            return obj.title_image.get_rendition(MEDIUM_FILTER_SPEC).url

    def get_languages(self, obj):
        """Return a list of language tags as strings."""
        return [language.i18n_title for language in obj.language_tags.all()]

    def get_genres(self, obj):
        """Return a list of genre tags as strings."""
        return [genre.i18n_title for genre in obj.genre_tags.all()]

    def get_periods(self, obj):
        """Return a list of literary period tags as strings."""
        return [period.i18n_title for period in obj.literary_period_tags.all()]

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
    tags = serializers.SerializerMethodField()
    authors = serializers.SerializerMethodField()
    coordinates = serializers.SerializerMethodField()
    created = serializers.ReadOnlyField(source="last_published_at")

    def get_authors(self, obj):
        """Return a list of primary keys of related authors."""
        return [author.pk for author in obj.authors.all()]

    def get_tags(self, obj):
        """Return a list of memorial type tags as string."""
        return [tag.i18n_title for tag in obj.memorial_type_tags.all()]

    def get_coordinates(self, obj):
        """Return memorial coordinates as a list."""
        return list(obj.coordinates.coords)

    class Meta:
        model = TempLocation
        fields = (
            "id",
            "title",
            "tags",
            "authors",
            "coordinates",
            "created"
        )


class MemorialDetailSerializer(MemorialSerializer):
    """Serializes Memorial pages to flat JSON objects output to detail views."""

    address = serializers.ReadOnlyField(source="i18n_address")
    desc = serializers.ReadOnlyField(source="i18n_introduction")

    class Meta:
        model = TempLocation
        fields = ("id", "title", "tags", "address", "desc", "authors", "coordinates", "created")