"""Custom filters that can be used to drill down the domain models."""

import django_filters
from django.utils.encoding import force_text
from django.utils.translation import gettext_lazy as _
from rest_framework.compat import coreapi, coreschema
from rest_framework.filters import BaseFilterBackend

from cms.models import Author, GenreTag, LanguageTag, Memorial, MemorialTag, PeriodTag


class WagtailSearchFilterBackend(BaseFilterBackend):
    """Filter backend that defers search queries to the Wagtail pages' search queryset method."""

    search_title = _("Search")
    search_description = _("A search term.")
    search_param = "q"
    template = "rest_framework/filters/search.html"

    def get_search_terms(self, request):
        """Return a list of search terms extracted from the request."""
        params = request.query_params.get(self.search_param, "")
        return params.replace(",", " ").split()

    def filter_queryset(self, request, queryset, view):
        """Add each search term to current querysets filter annotations."""
        search_terms = self.get_search_terms(request)
        for search_term in search_terms:
            queryset = queryset.search(search_term)
        return queryset

    def get_schema_fields(self, view):
        """Return schema entry for documentation."""
        return [
            coreapi.Field(
                name=self.search_param,
                required=False,
                location="search",
                schema=coreschema.String(
                    title=force_text(self.search_title),
                    description=force_text(self.search_description),
                ),
            )
        ]


class SearchResultFilter(django_filters.rest_framework.FilterSet):
    """Custom filters to go with our generic search view."""

    CHOICES = (
        ("author", _("Author")),
        ("memorial", _("Memorial")),
    )

    type = django_filters.ChoiceFilter(
        field_name="content_type__model",
        choices=CHOICES,
        label=_("Content type"),
        help_text=_("One of 'author' or 'memorial'."),
    )

    class Meta:
        fields = ("type",)


class AuthorFilter(django_filters.rest_framework.FilterSet):
    """Author specific filter implementation."""

    gender = django_filters.ChoiceFilter(
        field_name="sex",
        choices=Author.GENDER_CHOICES,
        label=_("Gender"),
        help_text=_("Gender of the author."),
    )
    yob = django_filters.RangeFilter(
        field_name="date_of_birth_year",
        label=_("Year of birth"),
        help_text=_(
            "Used to filter authors year of birth. "
            "A discrete value may be given. "
            "A range may be defined by appending _min or _max to the parameter name."
        ),
    )
    yod = django_filters.RangeFilter(
        field_name="date_of_death_year",
        label=_("Year of death"),
        help_text=_(
            "Used to filter author by year of death. " "See yob for more information."
        ),
    )
    language = django_filters.MultipleChoiceFilter(
        field_name="language_tags__title",
        choices=LanguageTag.objects.values_list("title", "title"),
        label=_("Languages"),
        help_text=_("Languages the author has been active in."),
    )
    genre = django_filters.ModelMultipleChoiceFilter(
        field_name="genre_tags",
        queryset=GenreTag.objects.all(),
        label=_("Genres"),
        help_text=_("Genres the author has been active in."),
    )
    period = django_filters.ModelMultipleChoiceFilter(
        field_name="literary_period_tags",
        queryset=PeriodTag.objects.all(),
        label=_("Literary periods"),
        help_text=_("Literary periods the author has been active in."),
    )

    class Meta:
        model = Author
        fields = ("gender", "yob", "yod", "language", "genre", "period")


class MemorialFilter(django_filters.rest_framework.FilterSet):
    """Memorial specific filter implementation."""

    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="memorial_type_tags",
        queryset=MemorialTag.objects.all(),
        label=_("Tags"),
        help_text=_("Tags that describe the memorial type."),
    )

    class Meta:
        model = Memorial
        fields = ("tags",)
