"""CMS url mappings."""
from django.conf.urls import url
from django.urls import path
from wagtail.images.views.serve import ServeView

from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path(
        'autocomplete/author/',
        views.AuthorAutocompleteView.as_view(),
        name='autocomplete-author',
    ),
    path(
        'autocomplete/language/',
        views.LanguageAutocomplete.as_view(),
        name='autocomplete-language',
    ),
    path(
        'autocomplete/location-type/',
        views.LocationTypeAutocomplete.as_view(),
        name='autocomplete-location-type',
    ),
    path(
        'autocomplete/genre/',
        views.GenreAutocomplete.as_view(),
        name='autocomplete-genre',
    ),
    path(
        'autocomplete/literary-period/',
        views.LiteraryPeriodAutocomplete.as_view(),
        name='autocomplete-literary-period',
    ),
    path(
        'autocomplete/age-group/',
        views.AgeGroupAutocomplete.as_view(),
        name='autocomplete-age-group',
    ),
    url(
        r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$',
        ServeView.as_view(action='redirect'),
        name='wagtailimages_serve',
    ),
]
