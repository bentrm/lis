"""Custom block types that the user content can be represented in."""

from django.utils.translation import gettext_lazy as _
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

RICH_TEXT_FEATURES_FOOTNOTE = [
    "bold",
    "italic",
    "strikethrough",
    "link",
]
RICH_TEXT_FEATURES_CONTENT = [
    "bold",
    "italic",
    "strikethrough",
    "footnote",
    "ol",
    "ul",
    "hr",
    "link",
    "blockquote",
]


class FootnoteStructBlock(blocks.StructBlock):
    """A structured block to model a linkable footnote."""

    tag = blocks.CharBlock(
        required=False,
        label=_("Linkable tag"),
        help_text=_(
            "A tag that allows to link the footnote "
            "with the paragraphs text content in the form '[tag]'."
        )
    )
    footnote = blocks.RichTextBlock(
        features=RICH_TEXT_FEATURES_FOOTNOTE,
        label=_("Footnote"),
        help_text=_("Citations, comments and references."))

    class Meta:
        label = _("Footnote")
        form_classname = "footnote-struct-block struct-block"
        template = "cms/blocks/footnote_struct_block.html"


class ParagraphStructBlock(blocks.StructBlock):
    """
    A structured block of content.

    Maps the 'HeadingWithContent' domain model entity to a Wagtail entity.
    """

    heading = blocks.CharBlock(
        required=False,
        label=_("Optional heading"),
        help_text=_("An optional heading to structure comprehensive text content."))
    images = blocks.ListBlock(
        ImageChooserBlock(),
        default=[],
        label=_("Images"),
        help_text=_("Images that will be displayed alongside the text content of the paragraph."))
    content = blocks.RichTextBlock(
        required=True,
        features=RICH_TEXT_FEATURES_CONTENT,
        label=_("Content"),
        help_text=_("The actual text content of this paragraph."))
    footnotes = blocks.ListBlock(
        FootnoteStructBlock(),
        default=[],
        label=_("Footnotes"),
        help_text=_("Optional footnotes to the text content."))
    editor = blocks.CharBlock(
        required=True,
        label=_("Editor"),
        help_text=_("Author or translator of the content."))

    class Meta:
        label = _("Paragraph")
        form_classname = "paragraph-struct-block struct-block"
        template = "cms/blocks/paragraph_struct_block.html"
