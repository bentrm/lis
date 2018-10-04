"""Custom wagtail hooks."""

from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from .models import APIKey


class ApiKeyModelAdmin(ModelAdmin):
    """Generic tag admin class."""

    model = APIKey
    menu_icon = "cogs"
    list_display = ("name", "key", "created", "get_status")
    search_fields = ("name",)
    ordering = ("name",)


class AdminGroup(ModelAdminGroup):
    """Tag group that groups all domain tag models."""

    menu_label = _("Admin")
    menu_icon = "cogs"
    menu_order = 300
    items = (ApiKeyModelAdmin,)


modeladmin_register(AdminGroup)
