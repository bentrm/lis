"""Custom permissions to guard the API agains external requests."""

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

        api_key = request.META.get("HTTP_AUTHORIZATION", "")
        if not api_key.startswith("Bearer "):
            return False

        return APIKey.objects.filter(key=api_key.replace("Bearer ", "")).exists()
