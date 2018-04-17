"""Custom block types that the user content can be represented in."""

from django.utils.translation import ugettext as _
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class ParagraphStructBlock(blocks.StructBlock):
    images = blocks.ListBlock(ImageChooserBlock())
    content = blocks.RichTextBlock(
        required=True,
        features=[
            "bold",
            "italic",
            "strikethrough",
            "sup",
            "ol",
            "ul",
            "hr",
            "link",
            "blockquote"
        ],
        help_text=_("Content of the text block."))
    footnotes = blocks.ListBlock(
        blocks.RichTextBlock(features=["bold", "italic", "strikethrough", "link"]),
        help_text=_("Citations and comments. The item number can be linked in the content, i.e. '[1]'.")
    )
    editor = blocks.CharBlock(
        required=True,
        help_text=_("Author or translator of the content."))
