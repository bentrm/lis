"""Custom filters that can be used to drill down the domain models."""

import django_filters
from django.template import loader
from django.utils.encoding import force_text
from django.utils.translation import gettext_lazy as _
from rest_framework.compat import coreapi, coreschema
from rest_framework.filters import BaseFilterBackend
from rest_framework.settings import api_settings

from cms.models import Author, MemorialTag
from cms.models import TempLocation as Memorial


class WagtailSearchFilterBackend(BaseFilterBackend):
    """Filter backend that defers search queries to the Wagtail pages' search queryset method."""

    search_title = _('Search')
    search_description = _('A search term.')
    search_param = api_settings.SEARCH_PARAM
    template = 'rest_framework/filters/search.html'

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

    def to_html(self, request, queryset, view):
        """Return HTML string to render input in docs."""
        if not getattr(view, 'search_fields', None):
            return ''

        term = self.get_search_terms(request)
        term = term[0] if term else ''
        context = {
            'param': self.search_param,
            'term': term
        }
        template = loader.get_template(self.template)
        return template.render(context)

    def get_schema_fields(self, view):
        """Return schema entry for documentation."""
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        return [
            coreapi.Field(
                name=self.search_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_text(self.search_title),
                    description=force_text(self.search_description)
                )
            )
        ]


class AuthorFilter(django_filters.rest_framework.FilterSet):
    """Author specific filter implementation."""

    gender = django_filters.ChoiceFilter(
        field_name="sex",
        choices=Author.GENDER_CHOICES,
        label=_("Gender"),
        help_text=_("Gender of the author.")
    )
    yob = django_filters.RangeFilter(
        field_name="date_of_birth_year",
        label=_("Year of birth"),
        help_text=_(
            "Used to filter authors year of birth. "
            "A discrete value may be given. "
            "A range may be defined by appending _min or _max to the parameter name."
        )
    )
    yod = django_filters.RangeFilter(
        field_name="date_of_death_year",
        label=_("Year of death"),
        help_text=_(
            "Used to filter author by year of death. "
            "See yob for more information."
        )
    )

    class Meta:
        model = Author
        fields = ("gender", "yob", "yod")


class MemorialFilter(django_filters.rest_framework.FilterSet):
    """Memorial specific filter implementation."""

    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="memorial_type_tags",
        queryset=MemorialTag.objects.all(),
        label=_("Tags"),
        help_text=_("Tags that describe the memorial type.")
    )

    class Meta:
        model = Memorial
        fields = ("tags",)
