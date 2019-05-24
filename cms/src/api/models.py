"""API related models."""

import binascii
import os

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


def generate_key():
    """Generate a random API key."""
    return binascii.hexlify(os.urandom(20)).decode()


class ApiKey(models.Model):
    """Represents an API key that will be used by client applications."""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, null=True, blank=False, on_delete=models.CASCADE)
    key = models.CharField(max_length=40, unique=True, blank=True, default=generate_key)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = _("API key")
        verbose_name_plural = _("API keys")
        ordering = ["-created"]
