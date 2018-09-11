from django.urls import include, path, re_path
from django.contrib.auth.models import User
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from . import views

urlpatterns = [
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("autocomplete/language/", views.LanguageAutocomplete.as_view(), name='autocomplete-language'),
    path("autocomplete/location-type/", views.LocationTypeAutocomplete.as_view(), name='autocomplete-location-type'),
    path("autocomplete/genre/", views.GenreAutocomplete.as_view(), name='autocomplete-genre'),
    path(
        "autocomplete/literary-period/",
        views.LiteraryPeriodAutocomplete.as_view(),
        name='autocomplete-literary-period'
    ),
    path(
        "autocomplete/contact-type/",
        views.ContactTypeAutocomplete.as_view(),
        name='autocomplete-contact-type'
    ),
    path("", include(wagtail_urls)),
]
