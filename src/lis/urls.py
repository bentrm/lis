"""Application wide URL config."""

from django.conf import settings
from django.urls import include, path
from rest_framework.documentation import include_docs_urls

api_url_patterns = [path("api/", include("api.urls"))]

urlpatterns = api_url_patterns + [
    path("i18n/", include("django.conf.urls.i18n")),
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "docs/",
        include_docs_urls(
            title="API",
            patterns=api_url_patterns,
            authentication_classes=[],
            permission_classes=[],
        ),
    ),
    path("", include("cms.urls")),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
