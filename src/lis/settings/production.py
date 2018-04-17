"""Producation settings."""

from __future__ import absolute_import, unicode_literals

from .base import *  # noqa

DEBUG = False

ALLOWED_HOSTS = [
    "www.lis-map.eu",
]

try:
    from .local import *  # noqa
except ImportError:
    pass
