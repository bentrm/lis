from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.urls import include, re_path, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

from search import views as search_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    re_path(r"^search/$", search_views.search, name="search"),
    re_path(r"^cms/", include(wagtailadmin_urls)),
    re_path(r"^documents/", include(wagtaildocs_urls)),
    re_path(r"^", include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
