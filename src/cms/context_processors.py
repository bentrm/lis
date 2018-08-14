from django.conf import settings
from .models import AuthorPage, LocationPage


def app_status(request):
    """Return the current application versions."""
    return {
        "CMS_VERSION": settings.CMS_VERSION,
        "AUTHOR_COUNT_PREVIEW": AuthorPage.objects.count(),
        "AUTHOR_COUNT_LIVE": AuthorPage.objects.live().count(),
        "MEMORIAL_SITE_COUNT_PREVIEW": LocationPage.objects.count(),
        "MEMORIAL_SITE_COUNT_LIVE": LocationPage.objects.live().count(),
    }
