"""All purpose module for helper functions and classes to validate, format and output data."""

import datetime

from django.utils.formats import date_format
from django.utils.translation import get_language
from django.utils.translation import gettext as _


class TranslatedField(object):
    """
    Helper class to add multilingual accessor properties to user content.

    Can be used to switch between different entity fields at runtime according to the
    selected user language. The output attribute is choosen by the current runtime
    language. Use django.util.translation.override to switch the language for the current
    context.

    If a default field is defined it will be returned if the field in the current runtime language
    is considered falsy.

    """

    def __init__(self, en_field: str, de_field: str, cs_field: str, default_field: str = None):
        self.en_field = en_field
        self.de_field = de_field
        self.cs_field = cs_field
        self.default_field = default_field

    @staticmethod
    def named(field: str, defaults_to_en: bool = False):
        """Return a new instance."""
        default_field = field if defaults_to_en else None
        return TranslatedField(field, f"{field}_de", f"{field}_cs", default_field)

    def __get__(self, instance, owner):
        lang = get_language()
        default_value = getattr(instance, self.default_field) if self.default_field else ""
        if lang == "en":
            return getattr(instance, self.en_field) or default_value
        elif lang == "de":
            return getattr(instance, self.de_field) or default_value
        elif lang == "cs":
            return getattr(instance, self.cs_field) or default_value
        return default_value


def validate_date(year: int = None, month: int = None, day: int = None):
    """Validate a given date for semantic integrity."""
    if year and month and day:
        datetime.datetime(year, month, day)
    elif month and day:
        if month == 2 and day > 29:
            raise ValueError(_("February cannot have more than 29 days."))
        elif not month % 2 and day > 30:
            raise ValueError(_("Day is out of range for the indicated month."))


def format_date(year: int = None, month: int = None, day: int = None):
    """Format date input in localized human readable string."""
    if year and month and day:
        return date_format(
            datetime.datetime(year, month, day),
            format="DATE_FORMAT",
            use_l10n=True)
    elif year and month:
        return date_format(
            datetime.datetime(year, month, 1),
            format="YEAR_MONTH_FORMAT",
            use_l10n=True)
    elif year:
        return year
    return ""
