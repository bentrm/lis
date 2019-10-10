from django.db.models import Subquery, OuterRef
from rest_framework import serializers

from cms.models import MemorialTag, LanguageTag, GenreTag, PeriodTag, Author, Memorial, AuthorName, MemorialPath, \
    Level1Page, Level2Page, Level3Page
from cms.models.base import BlogPage
from cms.serializers import TranslationField, ImageSerializer


class BlogPageSerializer(serializers.ModelSerializer):
    title = TranslationField()

    class Meta:
        model = BlogPage
        fields = (
            'title',
            'slug',
        )


class BlogPageDetailSerializer(BlogPageSerializer):
    body = TranslationField()

    class Meta:
        model = BlogPage
        fields = (
            'title',
            'slug',
            'body',
        )


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
    title = TranslationField()
    first_name = TranslationField()
    last_name = TranslationField()
    birth_name = TranslationField()

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
    title_image = ImageSerializer()
    academic_title = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    birth_name = serializers.CharField(read_only=True)
    dob = serializers.IntegerField(source='date_of_birth_day')
    mob = serializers.IntegerField(source='date_of_birth_month')
    yob = serializers.IntegerField(source='date_of_birth_year')
    pob = serializers.CharField(source='place_of_death')
    dod = serializers.IntegerField(source='date_of_death_day')
    mod = serializers.IntegerField(source='date_of_death_month')
    yod = serializers.IntegerField(source='date_of_death_year')
    pod = serializers.CharField(source='place_of_death')

    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return obj.get_url()

    class Meta:
        fields = (
            'id',
            'slug',
            'title_image',
            'academic_title',
            'first_name',
            'last_name',
            'birth_name',
            'dob', 'mob', 'yob', 'pob',
            'dod', 'mod', 'yod', 'pod',
            'url',
        )
        model = Author


class AuthorDetailSerializer(AuthorListSerializer):
    also_known_as = serializers.SerializerMethodField()
    genres = GenreSerializer(source="genre_tags", many=True)
    languages = GenreSerializer(source="language_tags", many=True)
    periods = PeriodSerializer(source="literary_period_tags", many=True)
    levels = serializers.SerializerMethodField()

    def get_also_known_as(self, obj):
        names = obj.names.all()[1:]
        serializer = AuthorNameSerializer(instance=names, many=True)
        return serializer.data

    def get_levels(self, obj):
        value = {}

        if Level1Page.objects.child_of(obj).exists():
            value['discover'] = 'discover/'
        if Level2Page.objects.child_of(obj).exists():
            value['research'] = 'research/'
        if Level3Page.objects.child_of(obj).exists():
            value['material'] = 'material/'

        return value

    class Meta:
        fields = (
            'id',
            'slug',
            'title_image',
            'academic_title',
            'first_name',
            'last_name',
            'birth_name',
            'also_known_as',
            'memorials',
            'genres',
            'languages',
            'periods',
            'dob', 'mob', 'yob', 'pob',
            'dod', 'mod', 'yod', 'pod',
            'url',
            'levels',
        )
        model = Author


class MemorialListSerializer(TitleSerializerMixin):
    title_image = ImageSerializer()
    position = serializers.SerializerMethodField()
    memorial_types = MemorialTypeSerializer(source="memorial_type_tags", many=True)

    def get_position(self, obj):
        lat, lng = obj.coordinates.coords
        return round(lat, 4), round(lng, 4)

    class Meta:
        fields = (
            'id',
            'title_image',
            'name',
            'position',
            'memorial_types'
        )
        model = Memorial


class MemorialDetailSerializer(MemorialListSerializer):
    authors = serializers.SerializerMethodField()
    address = TranslationField()
    contact_info = TranslationField()
    directions = TranslationField()
    introduction = TranslationField()
    description = TranslationField()
    detailed_description = TranslationField()

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

    class Meta:
        fields = (
            "id",
            'title_image',
            "name",
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
    description = TranslationField()

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


class Level1Serializer(serializers.ModelSerializer):
    biography = TranslationField()
    works = TranslationField()

    class Meta:
        fields = (
            'id',
            'biography',
            'works',
        )
        model = Level1Page


class Level2Serializer(serializers.ModelSerializer):
    biography = TranslationField()
    works = TranslationField()
    reception = TranslationField()
    connections = TranslationField()
    full_texts = TranslationField()

    class Meta:
        fields = (
            'id',
            'biography',
            'works',
            'reception',
            'connections',
            'full_texts',
        )
        model = Level2Page


class Level3Serializer(serializers.ModelSerializer):
    primary_literature = TranslationField()
    testimony = TranslationField()
    secondary_literature = TranslationField()
    didactic_material = TranslationField()

    class Meta:
        fields = (
            'id',
            'primary_literature',
            'testimony',
            'secondary_literature',
            'didactic_material',
        )
        model = Level3Page
