from rest_framework_gis.fields import GeometryField
from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField
from wagtail.images.views.serve import generate_image_url

from cms.models import Author, Memorial, MemorialTag, LanguageTag, GenreTag, PeriodTag, AuthorName


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta:
        fields = (
            "name",
        )


class LanguageSerializer(TagSerializer):
    class Meta:
        fields = (
            "name",
        )
        model = LanguageTag


class GenreSerializer(TagSerializer):
    class Meta:
        fields = (
            "name",
        )
        model = GenreTag


class PeriodSerializer(TagSerializer):
    class Meta:
        fields = (
            "name",
        )
        model = PeriodTag


class MemorialTypeSerializer(TagSerializer):
    class Meta:
        fields = (
            "name",
        )
        model = MemorialTag


class ImageSerializerMixin(object):
    def get_image(self, obj):
        if obj.title_image:
            return generate_image_url(obj.title_image, 'max-1000x1000|jpegquality-60')

    def get_image_thumbnail(self, obj):
        if obj.title_image:
            return generate_image_url(obj.title_image, 'fill-250x250|jpegquality-60')

    def get_image_title(self, obj):
        if obj.title_image:
            return obj.title_image.i18n_title

    def get_image_caption(self, obj):
        if obj.title_image:
            return obj.title_image.i18n_caption


class AuthorNameSerializer(serializers.ModelSerializer):
    surname = serializers.CharField()
    given_name = serializers.CharField()
    born = serializers.CharField()

    author = ResourceRelatedField(
        read_only=True,
        model=Author
    )

    class Meta:
        model = AuthorName
        fields = (
            'author',
            'sort_order',
            'is_pseudonym',
            'surname',
            'given_name',
            'born',
        )


class AuthorSerializer(serializers.ModelSerializer, ImageSerializerMixin):
    name = serializers.CharField(read_only=True)
    image = serializers.SerializerMethodField()
    image_thumbnail = serializers.SerializerMethodField()
    image_title = serializers.SerializerMethodField()
    image_caption = serializers.SerializerMethodField()
    born_in = serializers.CharField(read_only=True)
    died_in = serializers.CharField(read_only=True)
    languages = ResourceRelatedField(
        source='language_tags',
        read_only=True,
        many=True,
        model=LanguageTag
    )
    genres = ResourceRelatedField(
        source='genre_tags',
        read_only=True,
        many=True,
        model=GenreTag
    )
    periods = ResourceRelatedField(
        source='literary_period_tags',
        read_only=True,
        many=True,
        model=PeriodTag
    )

    class Meta:
        model = Author
        fields = (
            'name',
            'names',
            'sex',
            'image',
            'image_thumbnail',
            'image_title',
            'image_caption',
            'date_of_birth_year',
            'date_of_birth_month',
            'date_of_birth_day',
            'born_in',
            'date_of_death_year',
            'date_of_death_month',
            'date_of_death_day',
            'died_in',
            'memorials',
            'languages',
            'genres',
            'periods',
        )

    class JSONAPIMeta:
        resource_name = 'authors'


class MemorialSerializer(serializers.ModelSerializer, ImageSerializerMixin):
    name = serializers.CharField(read_only=True)
    image = serializers.SerializerMethodField()
    image_thumbnail = serializers.SerializerMethodField()
    image_title = serializers.SerializerMethodField()
    image_caption = serializers.SerializerMethodField()
    intro = serializers.CharField()
    desc = serializers.CharField()
    details = serializers.CharField()
    postal = serializers.CharField()
    way = serializers.CharField()
    contact = serializers.CharField()
    geometry = GeometryField(source='coordinates',      precision=5, remove_duplicates=True)
    authors = ResourceRelatedField(
        source='remembered_authors',
        read_only=True,
        many=True,
    )
    memorial_types = ResourceRelatedField(
        source='memorial_type_tags',
        read_only=True,
        many=True,
    )

    class Meta:
        model = Memorial
        fields = (
            'name',
            'image',
            'image_thumbnail',
            'image_title',
            'image_caption',
            'intro',
            'desc',
            'details',
            'postal',
            'way',
            'contact',
            'geometry',
            'authors',
            'memorial_types',
        )
