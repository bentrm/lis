from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.urls import include, path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

from cms import views as cms_views

urlpatterns = [
    # django
    path("i18n/", include("django.conf.urls.i18n")),

    # wagtail
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),

    # cms
    path("signup/", cms_views.SignupView.as_view(), name="signup"),
    path("demo/", include(wagtail_urls)),

    path("", include("home.urls")),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
