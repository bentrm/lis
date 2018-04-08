from django.utils.translation import ugettext as _
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class TextBlock(blocks.StructBlock):
    heading = blocks.PageChooserBlock(
        required=True,
        target_model="cms.TextTypePage",
        help_text=_(""))
    images = blocks.ListBlock(ImageChooserBlock())
    content = blocks.RichTextBlock(
        required=False,
        features=[
            "bold",
            "italic",
            "strikethrough",
            "sup",
            "ol",
            "ul",
            "hr",
            "blockquote"])
    editor = blocks.CharBlock(help_text=_("Author or translator of the content."))

    class Meta:
        template = "cms/blocks/text_block.html"
