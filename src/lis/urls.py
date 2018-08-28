from django.conf import settings
from django.urls import include, path

urlpatterns = [
    # django
    path("i18n/", include("django.conf.urls.i18n")),
    path('accounts/', include('django.contrib.auth.urls')),
    path("", include("cms.urls")),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
