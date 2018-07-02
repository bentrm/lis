"""Custom media model implementations overriding Wagtail defaults."""

from django.db import models
from django.utils. translation import gettext_lazy as _
from wagtail.core.models import CollectionMember
from wagtail.images.models import AbstractImage, AbstractRendition
from wagtail.documents.models import AbstractDocument
from wagtail.search import index

from .helpers import TranslatedField
from .messages import TXT

class Media(models.Model):
    """
    Implements the basic Media interface used by media items as images and documents.

    """

    title_de = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name=_(TXT["media.title_de"])
    )
    title_cs = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name=_(TXT["media.title_cs"])
    )
    i18n_title = TranslatedField.named("title", True)

    # TODO: Remove this field.
    alt_title = models.CharField(
        max_length=1024,
        null=True, blank=True,
        verbose_name=_("Alternative title"),
        help_text=_("Title that may be shown in tooltips and is used by screen readers.")
    )
    alt_title_de = models.CharField(
        max_length=1024,
        null=True, blank=True,
        verbose_name=_("German alternative title")
    )
    alt_title_cs = models.CharField(
        max_length=1024,
        null=True, blank=True,
        verbose_name=_("Czech alternative title")
    )
    i18n_alt_title = TranslatedField("alt_title", "alt_title_de", "alt_title_cs")

    caption = models.CharField(
        max_length=1024,
        null=True, blank=True,
        verbose_name=_(TXT["media.caption"]),
        help_text=_(TXT["media.caption.help"])
    )
    caption_de = models.CharField(
        max_length=1024,
        null=True, blank=True,
        verbose_name=_(TXT["media.caption_de"]),
        help_text=_(TXT["media.caption_de.help"])
    )
    caption_cs = models.CharField(
        max_length=1024,
        null=True, blank=True,
        verbose_name=_(TXT["media.caption_cs"]),
        help_text=_(TXT["media.caption_cs.help"])
    )
    i18n_caption = TranslatedField.named("caption")

    admin_form_fields = (
        "title",
        "title_de",
        "title_cs",
        "file",
        "collection",
        "alt_title",
        "alt_title_de",
        "alt_title_cs",
        "caption",
        "caption_de",
        "caption_cs",
        "tags",
    )

    search_fields = CollectionMember.search_fields + [
        index.SearchField('title', partial_match=True, boost=10),
        index.FilterField('title'),
        index.SearchField('title_de', partial_match=True, boost=10),
        index.FilterField('title_de'),
        index.SearchField('title_cs', partial_match=True, boost=10),
        index.FilterField('title_cs'),
        index.SearchField('caption', partial_match=True, boost=2),
        index.FilterField('caption'),
        index.SearchField('caption_de', partial_match=True, boost=2),
        index.FilterField('caption_de'),
        index.SearchField('caption_cs', partial_match=True, boost=2),
        index.FilterField('caption_cs'),
        index.RelatedFields('tags', [
            index.SearchField('name', partial_match=True, boost=10),
        ]),
        index.FilterField('uploaded_by_user'),
    ]

    def __str__(self):
        return str(self.i18n_title)

    class Meta:
        abstract = True


class ImageMedia(Media, AbstractImage):
    """Custom image implementation to add meta data properties."""

    admin_form_fields = Media.admin_form_fields + (
        "focal_point_x",
        "focal_point_y",
        "focal_point_width",
        "focal_point_height",
    )

    class Meta:
        db_table = "image"


class ImageMediaRendition(AbstractRendition):
    """Custom image rendition implementation to link to our custom image model."""

    image = models.ForeignKey(
        ImageMedia,
        on_delete=models.CASCADE,
        related_name="renditions",
        verbose_name=_(TXT["rendition.image"]),
        help_text=_(TXT["rendition.image.help"]))

    class Meta:
        db_table = "image_rendition"
        unique_together = (
            ("image", "filter_spec", "focal_point_key"))


class DocumentMedia(Media, AbstractDocument):
    """Custom document implementation to add meta data properties."""

    class Meta:
        db_table = "document"
