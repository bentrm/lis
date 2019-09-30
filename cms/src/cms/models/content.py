"""Implements the domain specific models of the information system."""

from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.utils.translation import override
from wagtail.admin.edit_handlers import (
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core.fields import StreamField

from cms.blocks import ParagraphStructBlock, DidacticMaterialStructBlock
from cms.messages import TXT
from .base import (
    DB_TABLE_PREFIX,
    I18nPage,
    TextType)
from .helpers import TranslatedField


class LevelPage(I18nPage):
    """A simple mixin that adds methods to list the models text types as an iterable."""

    PAGE_TITLE = "Level page"

    parent_page_types = ["Author"]
    text_types = ()
    level_order = 0

    @classmethod
    def can_create_at(cls, parent):
        """Determine the valid location of the page in the page hierarchy."""
        return super(LevelPage, cls).can_create_at(
            parent
        ) and not parent.get_children().exact_type(cls)

    def serve(self, request, *args, **kwargs):
        """Defer to the parent pages serve method."""
        return self.get_parent().specific.serve(request, *args, *kwargs)

    def get_texts(self):
        """Return the text type fields of the page as an iterable."""
        texts = []
        for text_type in self.text_types:
            prop = getattr(self, text_type.field, None)
            if prop:
                texts.append(TextType(prop, text_type.heading))
        return texts

    def full_clean(self, *args, **kwargs):
        """Set default title."""
        with override("en"):
            self.title = gettext(self.PAGE_TITLE)
        with override("de"):
            self.title_de = gettext(self.PAGE_TITLE)
        with override("cs"):
            self.title_cs = gettext(self.PAGE_TITLE)
        super(LevelPage, self).full_clean(*args, **kwargs)

    def __str__(self):
        return str(self.i18n_title)

    class Meta:
        abstract = True


class Level1Page(LevelPage):
    """The 'Discover' page of the LIS domain."""

    PAGE_TITLE = TXT["level1"]

    text_types = (
        TextType("i18n_description", _(TXT["memorial_site"])),  # TODO: Refactor
        TextType("i18n_biography", _(TXT["level1.biography"])),
        TextType("i18n_works", _(TXT["level1.works"])),
    )
    level_order = 1

    biography = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        default=[],
        verbose_name=_(TXT["level1.biography"]),
        help_text=_(TXT["level1.biography.help"]),
    )
    biography_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level1.biography"]),
        help_text=_(TXT["level1.biography.help"]),
    )
    biography_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level1.biography"]),
        help_text=_(TXT["level1.biography.help"]),
    )
    i18n_biography = TranslatedField.named("biography")

    works = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level1.works"]),
        help_text=_(TXT["level1.works.help"]),
    )
    works_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level1.works"]),
        help_text=_(TXT["level1.works.help"]),
    )
    works_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level1.works"]),
        help_text=_(TXT["level1.works.help"]),
    )
    i18n_works = TranslatedField.named("works")

    english_panels = [StreamFieldPanel("biography"), StreamFieldPanel("works")]
    german_panels = [StreamFieldPanel("biography_de"), StreamFieldPanel("works_de")]
    czech_panels = [StreamFieldPanel("biography_cs"), StreamFieldPanel("works_cs")]
    edit_handler = TabbedInterface(
        [
            ObjectList(english_panels, heading=_(TXT["heading.en"])),
            ObjectList(german_panels, heading=_(TXT["heading.de"])),
            ObjectList(czech_panels, heading=_(TXT["heading.cs"])),
            ObjectList(I18nPage.meta_panels, heading=_(TXT["heading.meta"])),
        ]
    )

    class Meta:
        db_table = DB_TABLE_PREFIX + "level_1"
        verbose_name = _(TXT["level1"])


class Level2Page(LevelPage):
    """The 'Deepen' page of the LIS domain."""

    PAGE_TITLE = TXT["level2"]

    text_types = (
        TextType("i18n_detailed_description", _(TXT["memorial_site"])),
        TextType("i18n_biography", _(TXT["level2.biography"])),
        TextType("i18n_works", _(TXT["level2.works"])),
        TextType("i18n_reception", _(TXT["level2.reception"])),
        TextType("i18n_connections", _(TXT["level2.connections"])),
        TextType("i18n_full_texts", _(TXT["level2.full_texts"])),
    )
    level_order = 2

    biography = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.biography"]),
        help_text=_(TXT["level2.biography"]),
    )
    biography_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.biography"]),
        help_text=_(TXT["level2.biography.help"]),
    )
    biography_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.biography"]),
        help_text=_(TXT["level2.biography.help"]),
    )
    i18n_biography = TranslatedField.named("biography")

    works = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.works"]),
        help_text=_(TXT["level2.works.help"]),
    )
    works_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.works"]),
        help_text=_(TXT["level2.works.help"]),
    )
    works_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.works"]),
        help_text=_(TXT["level2.works.help"]),
    )
    i18n_works = TranslatedField.named("works")

    reception = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.reception"]),
        help_text=_(TXT["level2.reception.help"]),
    )
    reception_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.reception"]),
        help_text=_(TXT["level2.reception.help"]),
    )
    reception_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.reception"]),
        help_text=_(TXT["level2.reception.help"]),
    )
    i18n_reception = TranslatedField.named("reception")

    connections = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.connections"]),
        help_text=_(TXT["level2.connections.help"]),
    )
    connections_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.connections"]),
        help_text=_(TXT["level2.connections.help"]),
    )
    connections_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.connections"]),
        help_text=_(TXT["level2.connections.help"]),
    )
    i18n_connections = TranslatedField.named("connections")

    full_texts = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.full_texts"]),
        help_text=_(TXT["level2.full_texts.help"]),
    )
    full_texts_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.full_texts"]),
        help_text=_(TXT["level2.full_texts.help"]),
    )
    full_texts_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.full_texts"]),
        help_text=_(TXT["level2.full_texts.help"]),
    )
    i18n_full_texts = TranslatedField.named("full_texts")

    english_panels = [
        StreamFieldPanel("biography"),
        StreamFieldPanel("works"),
        StreamFieldPanel("reception"),
        StreamFieldPanel("connections"),
        StreamFieldPanel("full_texts"),
    ]
    german_panels = [
        StreamFieldPanel("biography_de"),
        StreamFieldPanel("works_de"),
        StreamFieldPanel("reception_de"),
        StreamFieldPanel("connections_de"),
        StreamFieldPanel("full_texts_de"),
    ]
    czech_panels = [
        StreamFieldPanel("biography_cs"),
        StreamFieldPanel("works_cs"),
        StreamFieldPanel("reception_cs"),
        StreamFieldPanel("connections_cs"),
        StreamFieldPanel("full_texts_cs"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(english_panels, heading=_(TXT["heading.en"])),
            ObjectList(german_panels, heading=_(TXT["heading.de"])),
            ObjectList(czech_panels, heading=_(TXT["heading.cs"])),
            ObjectList(I18nPage.meta_panels, heading=_(TXT["heading.meta"])),
        ]
    )

    class Meta:
        db_table = DB_TABLE_PREFIX + "level_2"
        verbose_name = _(TXT["level2"])


class Level3Page(LevelPage):
    """The 'Research' page of the LIS domain."""

    PAGE_TITLE = TXT["level3"]

    text_types = (
        TextType("i18n_primary_literature", _(TXT["level3.primary_literature"])),
        TextType("i18n_testimony", _(TXT["level3.testimony"])),
        TextType("i18n_secondary_literature", _(TXT["level3.secondary_literature"])),
        TextType("i18n_didactic_material", _(TXT["level3.didactic_material"])),
    )
    level_order = 3

    primary_literature = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.primary_literature"]),
        help_text=_(TXT["level3.primary_literature.help"]),
    )
    primary_literature_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.primary_literature"]),
        help_text=_(TXT["level3.primary_literature.help"]),
    )
    primary_literature_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.primary_literature"]),
        help_text=_(TXT["level3.primary_literature.help"]),
    )
    i18n_primary_literature = TranslatedField.named("primary_literature")

    testimony = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.testimony"]),
        help_text=_(TXT["level3.testimony.help"]),
    )
    testimony_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.testimony"]),
        help_text=_(TXT["level3.testimony.help"]),
    )
    testimony_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.testimony"]),
        help_text=_(TXT["level3.testimony.help"]),
    )
    i18n_testimony = TranslatedField.named("testimony")

    secondary_literature = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.secondary_literature"]),
        help_text=_(TXT["level3.secondary_literature.help"]),
    )
    secondary_literature_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.secondary_literature"]),
        help_text=_(TXT["level3.secondary_literature.help"]),
    )
    secondary_literature_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.secondary_literature"]),
        help_text=_(TXT["level3.secondary_literature.help"]),
    )
    i18n_secondary_literature = TranslatedField.named("secondary_literature")

    didactic_material = StreamField(
        [("material", DidacticMaterialStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.didactic_material"]),
        help_text=_(TXT["level3.didactic_material.help"])
    )
    didactic_material_de = StreamField(
        [("material", DidacticMaterialStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.didactic_material"]),
        help_text=_(TXT["level3.didactic_material.help"])
    )
    didactic_material_cs = StreamField(
        [("material", DidacticMaterialStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.didactic_material"]),
        help_text=_(TXT["level3.didactic_material.help"])
    )
    i18n_didactic_material = TranslatedField.named("didactic_material")

    english_panels = [
        StreamFieldPanel("primary_literature"),
        StreamFieldPanel("testimony"),
        StreamFieldPanel("secondary_literature"),
        StreamFieldPanel("didactic_material"),
    ]
    german_panels = [
        StreamFieldPanel("primary_literature_de"),
        StreamFieldPanel("testimony_de"),
        StreamFieldPanel("secondary_literature_de"),
        StreamFieldPanel("didactic_material_de"),
    ]
    czech_panels = [
        StreamFieldPanel("primary_literature_cs"),
        StreamFieldPanel("testimony_cs"),
        StreamFieldPanel("secondary_literature_cs"),
        StreamFieldPanel("didactic_material_cs"),
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(english_panels, heading=_(TXT["heading.en"])),
            ObjectList(german_panels, heading=_(TXT["heading.de"])),
            ObjectList(czech_panels, heading=_(TXT["heading.cs"])),
            ObjectList(I18nPage.meta_panels, heading=_(TXT["heading.meta"])),
        ]
    )

    class Meta:
        db_table = DB_TABLE_PREFIX + "level_3"
        verbose_name = _(TXT["level3"])

