from html.parser import HTMLParser

from django.db.models import Subquery, OuterRef
from rest_framework import serializers
from wagtail.images.views.serve import generate_image_url

from cms.models import MemorialTag, LanguageTag, GenreTag, PeriodTag, Author, Memorial, AuthorName, MemorialPath


class TextExtractor(HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = ""

    def handle_data(self, data):
        self.text += data

    @classmethod
    def extract_text(cls, data):
        self = cls()
        self.feed(data)
        self.close()
        return self.text


class RenditionField(serializers.Field):
    def __init__(self, operation='fill-100x100|jpegquality-40', **kwargs):
        super().__init__(**kwargs)
        self.operation = operation

    def to_representation(self, value):
        """
        Serialize the value's class name.
        """
        if value:
            return generate_image_url(value, self.operation)


class TitleSerializerMixin(serializers.ModelSerializer):
    name = serializers.CharField()


class LanguageSerializer(TitleSerializerMixin):
    class Meta:
        fields = ("id", "name")
        model = LanguageTag


class GenreSerializer(TitleSerializerMixin):
    class Meta:
        fields = ("id", "name")
        model = GenreTag


class PeriodSerializer(TitleSerializerMixin):
    class Meta:
        fields = ("id", "name")
        model = PeriodTag


class MemorialTypeSerializer(TitleSerializerMixin):
    class Meta:
        fields = ("id", "name")
        model = MemorialTag


class AuthorNameSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField(required=False)
    first_name = serializers.SerializerMethodField(required=False)
    last_name = serializers.SerializerMethodField()
    birth_name = serializers.SerializerMethodField(required=False)

    def get_title(self, obj):
        return obj.i18n_title

    def get_first_name(self, obj):
        return obj.i18n_first_name

    def get_last_name(self, obj):
        return obj.i18n_last_name

    def get_birth_name(self, obj):
        return obj.i18n_birth_name

    class Meta:
        fields = (
            "is_pseudonym",
            "title",
            "first_name",
            "last_name",
            "birth_name",
        )
        model = AuthorName


class AuthorListSerializer(serializers.ModelSerializer):
    academic_title = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    birth_name = serializers.CharField(read_only=True)
    thumb = RenditionField(source='title_image', operation='fill-250x250|jpegquality-60')
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return obj.get_url()

    class Meta:
        fields = (
            'id',
            'slug',
            'academic_title',
            'first_name',
            'last_name',
            'birth_name',
            'thumb',
            'url',
        )
        model = Author


class AuthorDetailSerializer(AuthorListSerializer):
    banner = RenditionField(source='title_image', operation='fill-800x400|jpegquality-60')
    also_known_as = serializers.SerializerMethodField()
    genres = GenreSerializer(source="genre_tags", many=True)
    languages = GenreSerializer(source="language_tags", many=True)
    periods = PeriodSerializer(source="literary_period_tags", many=True)

    def get_also_known_as(self, obj):
        names = obj.names.all()[1:]
        serializer = AuthorNameSerializer(instance=names, many=True)
        return serializer.data

    class Meta:
        fields = (
            'id',
            'slug',
            'academic_title',
            'first_name',
            'last_name',
            'birth_name',
            'thumb',
            'banner',
            'also_known_as',
            'memorials',
            'genres',
            'languages',
            'periods',
            'url',
        )
        model = Author


class MemorialListSerializer(TitleSerializerMixin):
    thumb = serializers.SerializerMethodField(required=False)
    position = serializers.SerializerMethodField()
    memorial_types = MemorialTypeSerializer(source="memorial_type_tags", many=True)

    def get_thumb(self, obj):
        if obj.title_image:
            return obj.title_image.get_rendition('fill-100x100|jpegquality-60').url

    def get_position(self, obj):
        return obj.coordinates.coords

    class Meta:
        fields = (
            'id',
            'name',
            'thumb',
            'position',
            'memorial_types'
        )
        model = Memorial


class MemorialDetailSerializer(MemorialListSerializer):
    banner = RenditionField(source='title_image', operation='fill-800x400|jpegquality-60')
    authors = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    contact_info = serializers.SerializerMethodField()
    directions = serializers.SerializerMethodField()
    introduction = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    detailed_description = serializers.SerializerMethodField()

    def get_authors(self, obj):
        popular_name_qs = AuthorName.objects.filter(author_id=OuterRef('pk')).order_by('sort_order')[:1]
        queryset = Author.objects.filter(memorials=obj).annotate(
            academic_title=Subquery(popular_name_qs.values('title')),
            first_name=Subquery(popular_name_qs.values('first_name')),
            last_name=Subquery(popular_name_qs.values('last_name')),
            birth_name=Subquery(popular_name_qs.values('birth_name')),
        ).select_related('title_image').live().public()
        serializer = AuthorListSerializer(queryset, many=True)
        return serializer.data

    def get_address(self, obj):
        if TextExtractor.extract_text(obj.i18n_address):
            return obj.i18n_address

    def get_contact_info(self, obj):
        if TextExtractor.extract_text(obj.i18n_contact_info):
            return obj.i18n_contact_info

    def get_directions(self, obj):
        if TextExtractor.extract_text(obj.i18n_directions):
            return obj.i18n_directions

    def get_introduction(self, obj):
        if TextExtractor.extract_text(obj.i18n_introduction):
            return obj.i18n_introduction

    def get_description(self, obj):
        return obj.i18n_description.stream_data if obj.i18n_description else []

    def get_detailed_description(self, obj):
        return obj.i18n_detailed_description.stream_data if obj.i18n_detailed_description else []

    class Meta:
        fields = (
            "id",
            "name",
            "thumb",
            'banner',
            "authors",
            "position",
            "memorial_types",
            "address",
            "contact_info",
            "directions",
            "introduction",
            "description",
            "detailed_description",
        )
        model = Memorial


class MemorialPathListSerializer(TitleSerializerMixin):

    description = serializers.SerializerMethodField()

    def get_description(self, obj):
        return obj.i18n_description

    class Meta:
        model = MemorialPath
        fields = (
            'id',
            'name',
            'description',
        )


class MemorialPathDetailSerializer(MemorialPathListSerializer):
    waypoints = serializers.SerializerMethodField()

    def get_waypoints(self, obj):
        queryset = obj.waypoints.order_by('sort_order')
        memorials = [x.memorial for x in queryset if x.memorial.live]
        serializer = MemorialListSerializer(memorials, many=True, read_only=True)
        return serializer.data

    class Meta:
        model = MemorialPath
        fields = (
            'id',
            'name',
            'description',
            'waypoints',
        )
