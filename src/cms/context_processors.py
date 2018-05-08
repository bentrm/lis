from django.conf import settings


def app_versions(request):
    """Return the current application versions."""
    return {
        "CMS_VERSION": settings.CMS_VERSION,
    }
