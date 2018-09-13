"""Defines all tag domain models of the lis system."""

from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField

from cms.messages import TXT

from .helpers import TranslatedField

DB_TABLE_PREFIX = "cms_tag_"
RICH_TEXT_FEATURES = ["bold", "italic", "strikethrough", "link"]


class Tag(models.Model):
    """
    Abstract base class for all tag implementations.

    Subclasses may add domain specific fields that will be used for querying.

    """

    title = models.CharField(
        verbose_name=_(TXT["tag.title"]),
        help_text=_(TXT["tag.title.help"]),
        max_length=1000,
        unique=True
    )
    title_de = models.CharField(
        verbose_name=_(TXT["tag.title_de"]),
        help_text=_(TXT["tag.title_de.help"]),
        max_length=1000,
        unique=True
    )
    title_cs = models.CharField(
        verbose_name=_(TXT["tag.title_cs"]),
        help_text=_(TXT["tag.title_cs.help"]),
        max_length=1000,
        unique=True
    )
    i18n_title = TranslatedField.named("title", True)

    description = RichTextField(
        blank=True,
        features=RICH_TEXT_FEATURES,
        verbose_name=_(TXT["tag.description"]),
        help_text=_(TXT["tag.description.help"])
    )
    description_de = RichTextField(
        blank=True,
        features=RICH_TEXT_FEATURES,
        verbose_name=_(TXT["tag.description"]),
        help_text=_(TXT["tag.description.help"])
    )
    description_cs = RichTextField(
        blank=True,
        features=RICH_TEXT_FEATURES,
        verbose_name=_(TXT["tag.description"]),
        help_text=_(TXT["tag.description.help"])
    )
    i18n_description = TranslatedField.named("description")

    panels = [
        MultiFieldPanel(
            heading=_(TXT["heading.en"]),
            children=[
                FieldPanel("title"),
                FieldPanel("description"),
            ],
        ),
        MultiFieldPanel(
            heading=_(TXT["heading.de"]),
            children=[
                FieldPanel("title_de"),
                FieldPanel("description_de"),
            ],
        ),
        MultiFieldPanel(
            heading=_(TXT["heading.cs"]),
            children=[
                FieldPanel("title_cs"),
                FieldPanel("description_cs"),
            ],
        ),
    ]

    def __str__(self):
        return str(self.i18n_title)

    class Meta:
        abstract = True
        ordering = ["title"]
        verbose_name = _(TXT["tag"])
        verbose_name_plural = _(TXT["tag.plural"])


class SortableTag(Tag):
    """Adds a sort order attribute to the tag model."""

    sort_order = models.IntegerField(
        verbose_name=_(TXT["tag.sort_order"]),
        help_text=_(TXT["tag.sort_order.help"]),
    )

    panels = Tag.panels + [
        FieldPanel("sort_order"),
    ]

    class Meta:
        abstract = True
        ordering = ["sort_order"]


class GenreTag(Tag):
    """Used to tag literary genres."""

    class Meta:
        db_table = DB_TABLE_PREFIX + "genre"
        verbose_name = _(TXT["genre"])
        verbose_name_plural = _(TXT["genre.plural"])


class LanguageTag(Tag):
    """Used to tag languages spoken by an author."""

    class Meta:
        db_table = DB_TABLE_PREFIX + "language"
        verbose_name = _(TXT["language"])
        verbose_name_plural = _(TXT["language.plural"])


class LocationTypeTag(Tag):
    """Used to tag memorials."""

    class Meta:
        db_table = DB_TABLE_PREFIX + "location_type"
        verbose_name = _(TXT["location_type"])
        verbose_name_plural = _(TXT["location_type.plural"])


class LiteraryPeriodTag(SortableTag):
    """Used to tag literary periods an author has been active in."""

    class Meta:
        db_table = DB_TABLE_PREFIX + "literary_period"
        verbose_name = _(TXT["literary_period"])
        verbose_name_plural = _(TXT["literary_period.plural"])


class AgeGroupTag(SortableTag):
    """Used to tag age groups."""

    class Meta:
        db_table = DB_TABLE_PREFIX + "age_group"
        verbose_name = _(TXT["age_group"])
        verbose_name_plural = _(TXT["age_group.plural"])
