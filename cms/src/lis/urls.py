"""Application wide URL config."""
import logging
from urllib.parse import unquote

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path, re_path
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

logger = logging.getLogger(__name__)

urlpatterns = [
    path('cms/accounts/', include('django.contrib.auth.urls')),
    path('cms/wagtail/', include(wagtail_urls)),
    path('cms/admin/', include(wagtailadmin_urls)),
    path('cms/documents/', include(wagtaildocs_urls)),
    path('cms/preview/', include('cms.urls')),
]

urlpatterns += i18n_patterns(
    path('api/', include('api.urls')), prefix_default_language=False
)


if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
