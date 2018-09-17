"""Custom permissions to guard the API agains external requests."""

from django.db.models import F
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions

from .models import APIKey


class HasAPIAccess(permissions.BasePermission):
    """Checks the request for a valid api key."""

    message = _("Invalid or missing API Key.")

    def has_permission(self, request, view):
        """Return true of request headers include valid API key."""

        if request.user.is_authenticated:
            return True

        api_key = request.META.get("HTTP_API_KEY", "")
        qs = APIKey.objects.filter(key=api_key)
        if qs.exists():
            qs.update(requests=F("requests") + 1)
            return True
        return False
