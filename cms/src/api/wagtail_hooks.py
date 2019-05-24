"""Custom wagtail hooks."""

from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from .throttling import ApiKeyThrottle
from .models import ApiKey


class ApiKeyModelAdmin(ModelAdmin):
    """Generic tag admin class."""

    model = ApiKey
    menu_icon = "cogs"
    list_display = ("user", "key", "created", "get_status")
    search_fields = ("user",)
    ordering = ("user",)

    def get_status(self, obj):
        """Return human readable status string."""
        num_requests = ApiKeyThrottle.get_requests_for_api_key(obj.key)
        output = []
        for ttl, max_requests, count in num_requests:
            interval_length = ""
            if ttl >= 3600:
                interval_length = f"{ttl / 3600:g}h"
            elif ttl >= 60:
                interval_length = f"{ttl / 60:g}min"
            output.append(f"{interval_length} {count}/{max_requests}")
        return ", ".join(output)


class AdminGroup(ModelAdminGroup):
    """Tag group that groups all domain tag models."""

    menu_label = _("Admin")
    menu_icon = "cogs"
    menu_order = 300
    items = (ApiKeyModelAdmin,)


modeladmin_register(AdminGroup)
