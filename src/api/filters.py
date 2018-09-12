import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework.settings import api_settings
from rest_framework.filters import BaseFilterBackend
from cms.models.tags import LocationTypeTag
from cms.models.pages import Author, TempLocation as Memorial

class WagtailSearchFilterBackend(BaseFilterBackend):
    search_param = api_settings.SEARCH_PARAM

    def get_search_terms(self, request):
        params = request.query_params.get(self.search_param, '')
        return params.replace(',', ' ').split()

    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        for search_term in search_terms:
            print(search_term)
            queryset = queryset.search(search_term)
        return queryset


class AuthorFilter(django_filters.rest_framework.FilterSet):
    gender = django_filters.ChoiceFilter(field_name="sex", choices=Author.GENDER_CHOICES, label=_("Gender"))
    yob = django_filters.RangeFilter(field_name="date_of_birth_year", label=_("Year of birth"))
    yod = django_filters.RangeFilter(field_name="date_of_death_year", label=_("Year of death"))

    class Meta:
        model = Author
        fields = ("gender", "yob", "yod")


class MemorialFilter(django_filters.rest_framework.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="memorial_type_tags",
        queryset=LocationTypeTag.objects.all()
    )

    class Meta:
        model = Memorial
        fields = ("tags",)
