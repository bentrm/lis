"""Add app status properties to request context."""

from django.conf import settings

from cms.models import HomePage
from cms.models import Author
from cms.models import Memorial


def app_status(request):
    """Return the current application versions."""
    return {
        "CMS_VERSION": settings.CMS_VERSION,
        "ROOT_MENU": HomePage.objects.first()
        .get_children()
        .live()
        .in_menu()
        .specific(),
    }
