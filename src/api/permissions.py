"""Custom permissions to guard the API agains external requests."""

from django.utils.translation import gettext_lazy as _
from rest_framework import permissions

from .models import ApiKey


class HasAPIAccess(permissions.BasePermission):
    """Checks the request for a valid api key."""

    message = _("Invalid or missing API Key.")

    def is_valid_key(self, key):
        return ApiKey.objects.filter(key=key).exists()

    def has_permission(self, request, view):
        """Return true of request headers include valid API key."""
        if request.user.is_authenticated:
            return True

        authorization_header = request.META.get("HTTP_AUTHORIZATION", "Bearer ").replace("Bearer ", "")
        authorization_param = request.GET.get("token", "")

        print(authorization_param)

        return self.is_valid_key(authorization_header) or self.is_valid_key(authorization_param)
