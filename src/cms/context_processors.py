from django.conf import settings
from .models import Author, Location


def app_status(request):
    """Return the current application versions."""
    return {
        "CMS_VERSION": settings.CMS_VERSION,
        "AUTHOR_COUNT_PREVIEW": Author.objects.count(),
        "AUTHOR_COUNT_LIVE": Author.objects.live().count(),
        "MEMORIAL_SITE_COUNT_PREVIEW": Location.objects.count(),
        "MEMORIAL_SITE_COUNT_LIVE": Location.objects.live().count(),
    }
