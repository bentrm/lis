from django.db.models import Case, When, Q, F
from django.utils.translation import get_language
from rest_framework.filters import SearchFilter
from rest_framework_json_api.django_filters import DjangoFilterBackend
from rest_framework_json_api.filters import OrderingFilter
from rest_framework_json_api.views import ReadOnlyModelViewSet

from api.filters import MemorialFilter, AuthorFilter, SpatialQueryParameterValidationFilter, BoundingBoxFilter, \
    DistanceFilter
from api.serializers import AuthorSerializer, MemorialSerializer, LanguageSerializer, PeriodSerializer, \
    MemorialTypeSerializer, GenreSerializer, AuthorNameSerializer
from cms.models import Memorial, LanguageTag, PeriodTag, GenreTag, MemorialTag, Author, AuthorName


class AuthorNameViewSet(ReadOnlyModelViewSet):
    queryset = AuthorName.objects.all()
    serializer_class = AuthorNameSerializer
    filterset_fields = (
        'is_pseudonym',
        'author',
    )
    ordering_fields = (
        'given_name',
        'surname',
        'born',
    )
    search_fields = (
        'given_name',
        'surname',
        'born',
    )

    def get_object(self):
        pk = self.kwargs.get('pk', None)
        if pk is not None:
            return self.get_queryset().get(id=pk)

        return super().get_object()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        language_code = get_language()

        # TODO: Reduce annotation logic into a generic package and use it with the models
        # objects manager.
        if language_code == 'en':
            return queryset.annotate(
                surname=F('last_name'),
                given_name=F('first_name'),
                born='birth_name',
            )
        elif language_code == 'de':
            return queryset.annotate(
                surname=Case(
                    When(
                        Q(last_name_de__isnull=False) & ~Q(last_name_de__exact=''),
                        then=F('last_name_de')
                    ),
                    default=F('last_name')
                ),
                given_name=Case(
                    When(
                        Q(first_name_de__isnull=False) & ~Q(first_name_de__exact=''),
                        then=F('first_name_de')
                    ),
                    default=F('first_name')
                ),
                born=Case(
                    When(
                        Q(birth_name_de__isnull=False) & ~Q(birth_name_de__exact=''),
                        then=F('birth_name_de')
                    ),
                    default=F('birth_name')
                )
            )
        elif language_code == 'cz':
            return queryset.annotate(
                surname=Case(
                    When(
                        Q(last_name_cz__isnull=False) & ~Q(last_name_cz__exact=''),
                        then=F('last_name_cz')
                    ),
                    default=F('last_name'),
                ),
                given_name=Case(
                    When(
                        Q(first_name_cz__isnull=False) & ~Q(first_name_cz__exact=''),
                        then=F('first_name_cz')
                    ),
                    default=F('first_name')
                ),
                born=Case(
                    When(
                        Q(birth_name_cz__isnull=False) & ~Q(birth_name_cz__exact=''),
                        then=F('birth_name_cz')
                    ),
                    default=F('birth_name')
                )
            )
        else:
            raise Exception('Unsupported language code.')



class AuthorViewSet(ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filterset_class = AuthorFilter
    ordering_fields = (
        'name',
        'born_in',
        'date_of_birth_year',
        'date_of_birth_month',
        'date_of_birth_day',
        'died_in',
        'date_of_death_year',
        'date_of_death_month',
        'date_of_death_day',
    )
    search_fields = [
        'name', 'born_in', 'died_in',
    ]

    def get_object(self):
        pk = self.kwargs.get('pk', None)
        if pk is not None:
            return self.get_queryset().get(id=pk)

        return super().get_object()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        language_code = get_language()

        if language_code == 'en':
            return queryset.annotate(
                name=F('title'),
                born_in='place_of_birth',
                died_in=F('place_of_death'),
            )
        elif language_code == 'de':
            return queryset.annotate(
                name=Case(
                    When(
                        Q(title_de__isnull=False) & ~Q(title_de__exact=''),
                        then=F('title_de')
                    ),
                    default=F('title')
                ),
                born_in=Case(
                    When(
                        Q(place_of_birth_de__isnull=False) & ~Q(place_of_birth_de__exact=''),
                        then=F('place_of_birth_de')
                    ),
                    default=F('place_of_birth')
                ),
                died_in=Case(
                    When(
                        Q(place_of_death_de__isnull=False) & ~Q(place_of_death_de__exact=''),
                        then=F('place_of_death_de')
                    ),
                    default=F('place_of_death')
                )
            )
        elif language_code == 'cz':
            return queryset.annotate(
                name=Case(
                    When(
                        Q(title_cz__isnull=False) & ~Q(title_cz__exact=''),
                        then=F('title_cz')
                    ),
                    default=F('title'),
                ), born_in=Case(
                    When(
                        Q(place_of_birth_cz__isnull=False) & ~Q(place_of_birth_cz__exact=''),
                        then=F('place_of_birth_cz')
                    ),
                    default=F('place_of_birth')
                ),
                died_in=Case(
                    When(
                        Q(place_of_death_cz__isnull=False) & ~Q(place_of_death_cz__exact=''),
                        then=F('place_of_death_cz')
                    ),
                    default=F('place_of_death')
                )
            )
        else:
            raise Exception('Unsupported language code.')


class MemorialViewSet(ReadOnlyModelViewSet):
    queryset = Memorial.objects.all()
    serializer_class = MemorialSerializer
    filter_backends = (
       SpatialQueryParameterValidationFilter,
       OrderingFilter,
       DjangoFilterBackend,
       BoundingBoxFilter,
       DistanceFilter,
       SearchFilter,
    )
    bbox_filter_field = 'coordinates'
    bbox_filter_include_overlapping = True
    distance_filter_field = 'coordinates'
    distance_filter_convert_meters = True
    filterset_class = MemorialFilter
    ordering_fields = (
        'name',
    )
    search_fields = [
        'name', 'intro', 'desc', 'details', 'postal', 'way',
    ]

    def get_object(self):
        pk = self.kwargs.get('pk', None)
        if pk is not None:
            return self.get_queryset().get(id=pk)

        return super().get_object()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        language_code = get_language()

        if language_code == 'en':
            return queryset.annotate(
                name=F('title'),
                intro='introduction',
                desc=F('description'),
                details=F('detailed_description'),
                postal=F('address'),
                way=F('directions'),
                contact=F('contact_info')
            )
        elif language_code == 'de':
            return queryset.annotate(
                name=Case(
                    When(
                        Q(title_de__isnull=False) & ~Q(title_de__exact=''),
                        then=F('title_de')
                    ),
                    default=F('title')
                ),
                intro=Case(
                    When(
                        Q(introduction_de__isnull=False) & ~Q(introduction_de__exact=''),
                        then=F('introduction_de')
                    ),
                    default=F('introduction')
                ),
                desc=Case(
                    When(
                        Q(description_de__isnull=False) & ~Q(description_de__exact=''),
                        then=F('description_de')
                    ),
                    default=F('description')
                ),
                details=Case(
                    When(
                        Q(detailed_description_de__isnull=False) & ~Q(detailed_description_de__exact=''),
                        then=F('detailed_description_de')
                    ),
                    default=F('detailed_description')
                ),
                postal=Case(
                    When(
                        Q(address_de__isnull=False) & ~Q(address_de__exact=''),
                        then=F('address_de')
                    ),
                    default=F('address')
                ),
                way=Case(
                    When(
                        Q(directions_de__isnull=False) & ~Q(directions_de__exact=''),
                        then=F('directions_de')
                    ),
                    default=F('directions')
                ),
                contact=Case(
                    When(
                        Q(contact_info_de__isnull=False) & ~Q(contact_info_de__exact=''),
                        then=F('contact_info_de')
                    ),
                    default=F('contact_info')
                )
            )
        elif language_code == 'cz':
            return queryset.annotate(
                name=Case(
                    When(
                        Q(title_cz__isnull=False) & ~Q(title_cz__exact=''),
                        then=F('title_cz')
                    ),
                    default=F('title'),
                ), intro=Case(
                    When(
                        Q(introduction_cz__isnull=False) & ~Q(introduction_cz__exact=''),
                        then=F('introduction_cz')
                    ),
                    default=F('introduction')
                ),
                desc=Case(
                    When(
                        Q(description_cz__isnull=False) & ~Q(description_cz__exact=''),
                        then=F('description_cz')
                    ),
                    default=F('description')
                ),
                details=Case(
                    When(
                        Q(detailed_description_cz__isnull=False) & ~Q(detailed_description_cz__exact=''),
                        then=F('detailed_description_cz')
                    ),
                    default=F('detailed_description')
                ),
                postal=Case(
                    When(
                        Q(address_cz__isnull=False) & ~Q(address_cz__exact=''),
                        then=F('address_cz')
                    ),
                    default=F('address')
                ),
                way=Case(
                    When(
                        Q(directions_cz__isnull=False) & ~Q(directions_cz__exact=''),
                        then=F('directions_cz')
                    ),
                    default=F('directions')
                ),
                contact=Case(
                    When(
                        Q(contact_info_cz__isnull=False) & ~Q(contact_info_cz__exact=''),
                        then=F('contact_info_cz')
                    ),
                    default=F('contact_info')
                )
            )
        else:
            raise Exception('Unsupported language code.')


class TagViewSet(ReadOnlyModelViewSet):
    ordering_fields = (
        'name',
    )
    search_fields = [
        'name',
    ]

    def get_object(self):
        pk = self.kwargs.get('pk', None)
        if pk is not None:
            return self.get_queryset().get(id=pk)

        return super().get_object()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        language_code = get_language()

        if language_code == 'en':
            return queryset.annotate(
                name=F('title'),
            )
        elif language_code == 'de':
            return queryset.annotate(
                name=Case(
                    When(
                        Q(title_de__isnull=False) & ~Q(title_de__exact=''),
                        then=F('title_de')
                    ),
                    default=F('title')
                ),
            )
        elif language_code == 'cz':
            return queryset.annotate(
                name=Case(
                    When(
                        Q(title_cz__isnull=False) & ~Q(title_cz__exact=''),
                        then=F('title_cz')
                    ),
                    default=F('title'),
                )
            )
        else:
            raise Exception('Unsupported language code.')


class LanguageViewSet(TagViewSet):
    queryset = LanguageTag.objects.all()
    serializer_class = LanguageSerializer


class GenreViewSet(TagViewSet):
    queryset = GenreTag.objects.all()
    serializer_class = GenreSerializer


class PeriodViewSet(TagViewSet):
    queryset = PeriodTag.objects.all()
    serializer_class = PeriodSerializer


class MemorialTypeViewSet(TagViewSet):
    queryset = MemorialTag.objects.all()
    serializer_class = MemorialTypeSerializer
