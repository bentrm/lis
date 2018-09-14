"""Custom media model implementations overriding Wagtail defaults."""

from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.core.models import CollectionMember
from wagtail.documents.models import AbstractDocument
from wagtail.images.models import AbstractImage, AbstractRendition
from wagtail.search import index

from ..messages import TXT
from .base import DB_TABLE_PREFIX
from .helpers import TranslatedField

RICH_TEXT_FEATURES = ["bold", "italic", "strikethrough", "link"]


class Media(models.Model):
    """Implements the basic Media interface used by media items as images and documents."""

    title_de = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_(TXT["media.title_de"])
    )
    title_cs = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_(TXT["media.title_cs"])
    )
    i18n_title = TranslatedField.named("title", True)

    search_fields = CollectionMember.search_fields + [
        index.SearchField("title", partial_match=True, boost=10),
        index.FilterField("title"),
        index.SearchField("title_de", partial_match=True, boost=10),
        index.FilterField("title_de"),
        index.SearchField("title_cs", partial_match=True, boost=10),
        index.FilterField("title_cs"),
        index.RelatedFields(
            "tags", [index.SearchField("name", partial_match=True, boost=10)]
        ),
        index.FilterField("uploaded_by_user"),
    ]

    def __str__(self):
        return str(self.i18n_title)

    class Meta:
        abstract = True


class ImageMedia(Media, AbstractImage):
    """Custom image implementation to add meta data properties."""

    caption = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        verbose_name=_(TXT["image_media.caption"]),
        help_text=_(TXT["image_media.caption.help"]),
    )
    caption_de = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        verbose_name=_(TXT["image_media.caption_de"]),
    )
    caption_cs = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        verbose_name=_(TXT["image_media.caption_cs"]),
    )
    i18n_caption = TranslatedField.named("caption")

    admin_form_fields = (
        "title",
        "title_de",
        "title_cs",
        "file",
        "collection",
        "caption",
        "caption_de",
        "caption_cs",
        "tags",
        "focal_point_x",
        "focal_point_y",
        "focal_point_width",
        "focal_point_height",
    )

    class Meta:
        db_table = DB_TABLE_PREFIX + "image"


class ImageMediaRendition(AbstractRendition):
    """Custom image rendition implementation to link to our custom image model."""

    image = models.ForeignKey(
        ImageMedia,
        on_delete=models.CASCADE,
        related_name="renditions",
        verbose_name=_(TXT["rendition.image"]),
        help_text=_(TXT["rendition.image.help"]),
    )

    class Meta:
        db_table = DB_TABLE_PREFIX + "image_rendition"
        unique_together = ("image", "filter_spec", "focal_point_key")


class DocumentMedia(Media, AbstractDocument):
    """Custom document implementation to add meta data properties."""

    summary = models.CharField(
        max_length=2000,
        null=True,
        blank=True,
        verbose_name=_(TXT["document_media.summary"]),
        help_text=_(TXT["document_media.summary.help"]),
    )
    summary_de = models.CharField(
        max_length=2000,
        null=True,
        blank=True,
        verbose_name=_(TXT["document_media.summary_de"]),
    )
    summary_cs = models.CharField(
        max_length=2000,
        null=True,
        blank=True,
        verbose_name=_(TXT["document_media.summary_cs"]),
    )
    i18n_summary = TranslatedField.named("summary")

    admin_form_fields = (
        "title",
        "title_de",
        "title_cs",
        "file",
        "collection",
        "summary",
        "summary_de",
        "summary_cs",
        "tags",
    )

    class Meta:
        db_table = DB_TABLE_PREFIX + "document"
