"""API related models."""

import binascii
import os

from django.db import models
from django.utils.translation import gettext_lazy as _


def generate_key():
    """Generate a random API key."""
    return binascii.hexlify(os.urandom(20)).decode()


class APIKey(models.Model):
    """Represents an API key that will be used by client applications."""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50, unique=True)
    key = models.CharField(max_length=40, unique=True, blank=True, default=generate_key)
    requests = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("API key")
        verbose_name_plural = _("API keys")
        ordering = ["-created"]
