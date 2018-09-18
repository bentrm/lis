"""API related models."""

import binascii
import os

from django.db import models
from django.utils.translation import gettext_lazy as _
from .throttling import ApiKeyThrottle


def generate_key():
    """Generate a random API key."""
    return binascii.hexlify(os.urandom(20)).decode()


class APIKey(models.Model):
    """Represents an API key that will be used by client applications."""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50, unique=True)
    key = models.CharField(max_length=40, unique=True, blank=True, default=generate_key)

    def get_status(self):
        """Return human readable status string."""
        num_requests = self.get_num_requests()
        output = []
        for ttl, max_requests, count in num_requests:
            interval_length = ""
            if ttl >= 3600:
                interval_length = f"{ttl / 3600:g}h"
            elif ttl >= 60:
                interval_length = f"{ttl / 60:g}min"
            output.append(f"{interval_length} {count}/{max_requests}")
        return ", ".join(output)

    def get_num_requests(self):
        """Return an array of rate/request-mappings."""
        return ApiKeyThrottle.get_requests_for_api_key(self.key)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("API key")
        verbose_name_plural = _("API keys")
        ordering = ["-created"]
