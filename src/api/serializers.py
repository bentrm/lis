from rest_framework import serializers
from cms.models import pages as models, tags

THUMBNAIL_FILTER_SPEC = "fill-300x300|jpegquality-60"
MEDIUM_FILTER_SPEC = "max-1000x1000|jpegquality-60"


class AuthorNameSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="i18n_title")
    first_name = serializers.CharField(source="i18n_first_name")
    last_name = serializers.CharField(source="i18n_last_name")
    birth_name = serializers.CharField(source="i18n_birth_name")
    pseudonym = serializers.BooleanField(source="is_pseudonym")

    class Meta:
        model = models.AuthorName
        fields = ("title", "first_name", "last_name", "birth_name", "pseudonym")


class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="i18n_title")
    gender = serializers.ReadOnlyField(source="sex")
    thumbnail = serializers.SerializerMethodField()
    created = serializers.ReadOnlyField(source="last_published_at")

    def get_thumbnail(self, obj):
        if obj.title_image:
            return obj.title_image.get_rendition(THUMBNAIL_FILTER_SPEC).url

    class Meta:
        model = models.Author
        fields = ("id", "name", "gender", "thumbnail", "born", "created")


class AuthorDetailSerializer(AuthorSerializer):
    cover = serializers.SerializerMethodField()
    names = AuthorNameSerializer(many=True, read_only=True)
    languages = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    periods = serializers.SerializerMethodField()

    def get_cover(self, obj):
        if obj.title_image:
            return obj.title_image.get_rendition(MEDIUM_FILTER_SPEC).url

    def get_languages(self, obj):
        return [language.i18n_title for language in obj.language_tags.all()]

    def get_genres(self, obj):
        return [genre.i18n_title for genre in obj.genre_tags.all()]

    def get_periods(self, obj):
        return [period.i18n_title for period in obj.literary_period_tags.all()]

    class Meta:
        model = models.Author
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
    title = serializers.ReadOnlyField(source="i18n_title")
    tags = serializers.SerializerMethodField()
    authors = serializers.SerializerMethodField()
    coordinates = serializers.SerializerMethodField()
    created = serializers.ReadOnlyField(source="last_published_at")

    def get_authors(self, obj):
        return [author.pk for author in obj.authors.all()]

    def get_tags(self, obj):
        return [tag.i18n_title for tag in obj.memorial_type_tags.all()]

    def get_coordinates(self, obj):
        return list(obj.coordinates.coords)

    class Meta:
        model = models.TempLocation
        fields = (
            "id",
            "title",
            "tags",
            "authors",
            "coordinates",
            "created"
        )

class MemorialDetailSerializer(MemorialSerializer):
    address = serializers.ReadOnlyField(source="i18n_address")
    desc = serializers.ReadOnlyField(source="i18n_introduction")

    class Meta:
        model = models.TempLocation
        fields = ("id", "title", "tags", "address", "desc", "authors", "coordinates", "created")
