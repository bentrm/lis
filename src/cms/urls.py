from django.urls import include, path
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from .views import GenreAutocomplete, LanguageAutocomplete, LiteraryPeriodAutocomplete, SignupView

urlpatterns = [
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("signup/", SignupView.as_view(), name="signup"),
    path("autocomplete/language/", LanguageAutocomplete.as_view(), name='autocomplete-language'),
    path("autocomplete/genre/", GenreAutocomplete.as_view(), name='autocomplete-genre'),
    path(
        "autocomplete/literary-period/",
        LiteraryPeriodAutocomplete.as_view(),
        name='autocomplete-literary-period'
    ),
    path("demo/", include(wagtail_urls)),
]
