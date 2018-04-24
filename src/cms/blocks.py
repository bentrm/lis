"""Custom block types that the user content can be represented in."""

from django.utils.translation import ugettext as _
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class ParagraphStructBlock(blocks.StructBlock):
    images = blocks.ListBlock(
        ImageChooserBlock(),
        label=_("Images"),
        help_text=_("Images that will be displayed alongside the text content of the paragraph."))
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
        label=_("Content"),
        help_text=_("The actual text content of this paragraph."))
    footnotes = blocks.ListBlock(
        blocks.RichTextBlock(features=["bold", "italic", "strikethrough", "link"]),
        label=_("Footnotes"),
        help_text=_("Citations, comments and references. The entry can be linked in the content box of the paragraph "
                    "by its respective identifier, i.e. '[1]'.")
    )
    editor = blocks.CharBlock(
        required=True,
        label=_("Editor"),
        help_text=_("Author or translator of the content."))

    class Meta:
        template = "cms/blocks/paragraph_struct_block.html"
