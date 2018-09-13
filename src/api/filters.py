"""Custom filters that can be used to drill down the domain models."""

import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework.filters import BaseFilterBackend
from rest_framework.settings import api_settings

from cms.models import Author, LocationTypeTag
from cms.models import TempLocation as Memorial


class WagtailSearchFilterBackend(BaseFilterBackend):
    """Filter backend that defers search queries to the Wagtail pages' search queryset method."""

    search_param = api_settings.SEARCH_PARAM

    def get_search_terms(self, request):
        """Return a list of search terms extracted from the request."""
        params = request.query_params.get(self.search_param, '')
        return params.replace(',', ' ').split()

    def filter_queryset(self, request, queryset, view):
        """Add each search term to current querysets filter annotations."""
        search_terms = self.get_search_terms(request)
        for search_term in search_terms:
            print(search_term)
            queryset = queryset.search(search_term)
        return queryset


class AuthorFilter(django_filters.rest_framework.FilterSet):
    """Author specific filter implementation."""

    gender = django_filters.ChoiceFilter(field_name="sex", choices=Author.GENDER_CHOICES, label=_("Gender"))
    yob = django_filters.RangeFilter(field_name="date_of_birth_year", label=_("Year of birth"))
    yod = django_filters.RangeFilter(field_name="date_of_death_year", label=_("Year of death"))

    class Meta:
        model = Author
        fields = ("gender", "yob", "yod")


class MemorialFilter(django_filters.rest_framework.FilterSet):
    """Memorial specific filter implementation."""

    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="memorial_type_tags",
        queryset=LocationTypeTag.objects.all()
    )

    class Meta:
        model = Memorial
        fields = ("tags",)
