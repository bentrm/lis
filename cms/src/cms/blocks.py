"""Custom block types that the user content can be represented in."""

from django.utils.translation import gettext_lazy as _
from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock

RICH_TEXT_FEATURES_FOOTNOTE = ["bold", "italic", "strikethrough", "link"]
RICH_TEXT_FEATURES_CONTENT = [
    "bold",
    "italic",
    "strikethrough",
    "footnote",
    "ol",
    "ul",
    "hr",
    "link",
    "document-link",
    "blockquote",
]


class CustomImageChooserBlock(ImageChooserBlock):
    def get_api_representation(self, value, context=None):
        # TODO: needed to guard against circular import
        from cms.serializers import ImageSerializer
        return ImageSerializer(context=context).to_representation(value)


class FootnoteStructBlock(blocks.StructBlock):
    """A structured block to model a linkable footnote."""

    tag = blocks.CharBlock(
        required=False,
        label=_("Linkable tag"),
        help_text=_(
            "A tag that allows to link the footnote "
            "with the paragraphs text content in the form '[tag]'."
        ),
    )
    footnote = blocks.RichTextBlock(
        features=RICH_TEXT_FEATURES_FOOTNOTE,
        label=_("Footnote"),
        help_text=_("Citations, comments and references."),
    )

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
        help_text=_("An optional heading to structure comprehensive text content."),
    )
    images = blocks.ListBlock(
        CustomImageChooserBlock(),
        default=[],
        label=_("Images"),
        help_text=_(
            "Images that will be displayed alongside the text content of the paragraph."
        ),
    )
    content = blocks.RichTextBlock(
        required=True,
        features=RICH_TEXT_FEATURES_CONTENT,
        label=_("Content"),
        help_text=_("The actual text content of this paragraph."),
    )
    footnotes = blocks.ListBlock(
        FootnoteStructBlock(),
        default=[],
        label=_("Footnotes"),
        help_text=_("Optional footnotes to the text content."),
    )
    editor = blocks.CharBlock(
        required=True,
        label=_("Editor"),
        help_text=_("Author or translator of the content."),
    )

    class Meta:
        label = _("Paragraph")
        form_classname = "paragraph-struct-block struct-block"
        template = "cms/blocks/paragraph_struct_block.html"


class APIDocumentChooserBlock(DocumentChooserBlock):
    def get_api_representation(self, value, context=None):
        from cms.serializers import DocumentSerializer
        return DocumentSerializer(context=context).to_representation(value)


class DidacticMaterialStructBlock(blocks.StructBlock):
    heading = blocks.CharBlock(
        required=True,
        label=_("Heading"),
        help_text=_("A heading that describes the linked document replacing or complementing the files title."),
    )
    document = APIDocumentChooserBlock(
        required=True,
        label=_("Document"),
    )
    content = blocks.RichTextBlock(
        required=False,
        features=RICH_TEXT_FEATURES_CONTENT,
        label=_("Content"),
        help_text=_("A description of the documents content."),
    )
    footnotes = blocks.ListBlock(
        FootnoteStructBlock(),
        default=[],
        label=_("Footnotes"),
        help_text=_("Optional footnotes that can be linked in the content description."),
    )
    editor = blocks.CharBlock(
        required=True,
        label=_("Editor"),
        help_text=_("Author or translator of the content."),
    )

    class Meta:
        label = _("Document")
        form_classname = "didactic-material-struct-block struct-block"
        template = "cms/blocks/didactic_material_struct_block.html"
