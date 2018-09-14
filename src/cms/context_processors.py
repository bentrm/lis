from django.conf import settings

from .models import Author, HomePage, Memorial


def app_status(request):
    """Return the current application versions."""

    return {
        "CMS_VERSION": settings.CMS_VERSION,
        "ROOT_MENU": HomePage.objects.first()
        .get_children()
        .live()
        .in_menu()
        .specific(),
        "AUTHOR_COUNT": Author.objects.count(),
        "MEMORIAL_SITE_COUNT": Memorial.objects.count(),
    }
