from rest_framework import serializers

from cms.models import MemorialTag, LanguageTag, GenreTag, PeriodTag, Author, Memorial, AuthorName


class TitleSerializerMixin(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.i18n_title


class LanguageSerializer(TitleSerializerMixin):
    class Meta:
        fields = ("id", "title")
        model = LanguageTag


class GenreSerializer(TitleSerializerMixin):
    class Meta:
        fields = ("id", "title")
        model = GenreTag


class PeriodSerializer(TitleSerializerMixin):
    class Meta:
        fields = ("id", "title")
        model = PeriodTag


class MemorialTypeSerializer(TitleSerializerMixin):
    class Meta:
        fields = ("id", "title")
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


class AuthorSerializer(serializers.ModelSerializer):
    academic_title = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    birth_name = serializers.CharField(read_only=True)
    thumb = serializers.SerializerMethodField(required=False)
    also_known_as = serializers.SerializerMethodField()
    genres = GenreSerializer(source="genre_tags", many=True)
    languages = GenreSerializer(source="language_tags", many=True)
    periods = PeriodSerializer(source="literary_period_tags", many=True)
    url = serializers.SerializerMethodField()

    def get_name(self, obj):
        name = obj.names.first()
        serializer = AuthorNameSerializer(instance=name)
        return serializer.data

    def get_thumb(self, obj):
        if obj.title_image:
            return obj.title_image.get_rendition('fill-100x100|jpegquality-60').url

    def get_also_known_as(self, obj):
        names = obj.names.all()[1:]
        serializer = AuthorNameSerializer(instance=names, many=True)
        return serializer.data

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
            'also_known_as',
            'genres',
            'languages',
            'periods',
            'url',
        )
        model = Author


class AuthorListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def get_name(self, obj):
        name = obj.names.first()
        serializer = AuthorNameSerializer(instance=name)
        return serializer.data

    def get_url(self, obj):
        return obj.get_url()

    class Meta:
        fields = (
            'id',
            'name',
            'url',
        )
        model = Author


class PositionSerializer(TitleSerializerMixin):
    position = serializers.SerializerMethodField()

    def get_position(self, obj):
        return obj.coordinates.coords

    class Meta:
        fields = (
            'id',
            'title',
            'position'
        )
        model = Memorial


class MemorialSerializer(TitleSerializerMixin):
    thumb = serializers.SerializerMethodField(required=False)
    position = serializers.SerializerMethodField()
    authors = AuthorListSerializer(source="remembered_authors", many=True)
    memorial_types = MemorialTypeSerializer(source="memorial_type_tags", many=True)
    address = serializers.SerializerMethodField()
    contact_info = serializers.SerializerMethodField()
    directions = serializers.SerializerMethodField()
    introduction = serializers.SerializerMethodField()
    # description = serializers.SerializerMethodField()
    # detailed_description = serializers.SerializerMethodField()

    def get_thumb(self, obj):
        if obj.title_image:
            return obj.title_image.get_rendition('fill-100x100|jpegquality-60').url

    def get_position(self, obj):
        return obj.coordinates.coords

    def get_address(self, obj):
        return obj.i18n_address

    def get_contact_info(self, obj):
        return obj.i18n_contact_info

    def get_directions(self, obj):
        return obj.i18n_directions

    def get_introduction(self, obj):
        return obj.i18n_introduction

    # def get_description(self, obj):
    #     return obj.description
    #
    # def get_detailed_description(self, obj):
    #     return obj.detailed_description

    class Meta:
        fields = (
            "id",
            "title",
            "thumb",
            "authors",
            "position",
            "memorial_types",
            "address",
            "contact_info",
            "directions",
            "introduction",
            # "description",
            # "detailed_description",
        )
        model = Memorial


class AuthorFilterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "pk",
            "title",
            "title_de",
            "title_cs",
        )
        model = Author
