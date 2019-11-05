"""Application wide URL config."""
import logging
from urllib.parse import unquote

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import include, path, re_path
from django.utils.http import is_safe_url
from django.utils.translation import (LANGUAGE_SESSION_KEY, check_for_language)
from django.views.generic import TemplateView
from django.views.i18n import LANGUAGE_QUERY_PARAMETER
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

logger = logging.getLogger(__name__)


def set_language(request):
    """
    Redirect to a given URL while setting the chosen language in the session
    (if enabled) and in a cookie. The URL and the language code need to be
    specified in the request parameters.

    Since this view changes how the user will see the rest of the site, it must
    only be accessed as a POST request. If called as a GET request, it will
    redirect to the page in the request (the 'next' parameter) without changing
    any state.
    """
    next = request.POST.get('next', request.GET.get('next'))
    host = request.get_host()
    is_secure = request.is_secure()

    if ((next or not request.is_ajax()) and
            not is_safe_url(url=next, allowed_hosts={host}, require_https=is_secure)):
        next = request.META.get('HTTP_REFERER')
        next = next and unquote(next)  # HTTP_REFERER may be encoded.
        if not is_safe_url(url=next, allowed_hosts={host}, require_https=is_secure):
            logger.warning(f"Referrer {next} not safe to redirect, falling back to '/'")
            next = '/'

    response = HttpResponseRedirect(next) if next else HttpResponse(status=204)
    if request.method == 'POST':
        lang_code = request.POST.get(LANGUAGE_QUERY_PARAMETER)
        if lang_code and check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session[LANGUAGE_SESSION_KEY] = lang_code
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME, lang_code,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                domain=settings.LANGUAGE_COOKIE_DOMAIN,
            )
        else:
            logger.warning(f"Language code {lang_code} not found.")

    return response


urlpatterns = [
    path('i18n/setlang/', set_language, name='set_language'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('wagtail/', include(wagtail_urls)),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('api/', include('api.urls')),
    path('cms/', include('cms.urls')),
]


if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

# Catch all patterns to serve SPA
urlpatterns += (
    path('', TemplateView.as_view(template_name='app/index.html'), name='index'),
    re_path(r'^.*/', TemplateView.as_view(template_name='app/index.html'), name='index'),
)
