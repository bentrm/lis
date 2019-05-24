import os

from django.core.exceptions import ImproperlyConfigured


def env(NAME, default=None, required=False, parse_to_bool=False):
    """Return env variable or default value."""
    value = os.environ.get(NAME, default)

    if value is None and required:
        raise ImproperlyConfigured(f"Setting {NAME} is required but unset.")

    if parse_to_bool:
        if value in ("True", "true", "t", "1", True):
            return True
        elif value in ("False", "false", "f", "0", False):
            return False
        else:
            raise ImproperlyConfigured(f"Setting {NAME} is required to be a boolean.")

    return value
