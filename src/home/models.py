import logging

from django.contrib.gis.db.models import PointField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import text, translation
from django.utils.translation import ugettext_lazy as _
from mapwidgets import GooglePointFieldWidget
from modelcluster.fields import ParentalKey
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField

from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, TabbedInterface, ObjectList, StreamFieldPanel, \
    PageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index

logger = logging.getLogger('wagtail.core')

BLANK_TEXT = "_blank"
LEVEL_DISCOVER = "I"
LEVEL_DEEPEN = "II"
LEVEL_RESEARCH = "III"
LEVEL_CHOICES = (
    (LEVEL_DISCOVER, _("I. Discover")),
    (LEVEL_DEEPEN, _("II. Deepen")),
    (LEVEL_RESEARCH, _("III. Research")),
)


class TranslatedField(object):
    def __init__(self, en_field, de_field, cz_field):
        self.en_field = en_field
        self.de_field = de_field
        self.cz_field = cz_field

    def __get__(self, instance, owner):
        lang = translation.get_language()
        if lang == "de":
            return getattr(instance, self.de_field)
        if lang == "cz":
            return getattr(instance, self.cz_field)
        else:
            return getattr(instance, self.en_field)


class Describable(models.Model):
    description = models.TextField(blank=True)
    description_de = models.TextField(blank=True)
    description_cz = models.TextField(blank=True)

    i18n_description = TranslatedField("description", "description_de", "description_cz")

    class Meta:
        abstract = True


class Name(models.Model):
    title = models.CharField(max_length=255, blank=True, help_text=_("The academic title of the author."))
    title_de = models.CharField(max_length=255, blank=True, help_text=_("The academic title of the author."))
    title_cz = models.CharField(max_length=255, blank=True, help_text=_("The academic title of the author."))
    i18n_title = TranslatedField("title", "title_de", "title_cz")

    first_name = models.CharField(max_length=255, blank=True)
    first_name_de = models.CharField(max_length=255, blank=True)
    first_name_cz = models.CharField(max_length=255, blank=True)
    i18n_first_name = TranslatedField("first_name", "first_name_de", "first_name_cz")

    last_name = models.CharField(max_length=255, blank=True)
    last_name_de = models.CharField(max_length=255, blank=True)
    last_name_cz = models.CharField(max_length=255, blank=True)
    i18n_last_name = TranslatedField("last_name", "last_name_de", "last_name_cz")

    is_birth_name = models.BooleanField(default=True)
    is_pseudonym = models.BooleanField(default=False)

    def clean(self):
        super(Name, self).clean()
        if not self.first_name and not self.last_name:
            raise ValidationError(_("Name entries must at least define a first name or a last name."))

    def full_name(self):
        return " ".join(x.strip() for x in [self.title, self.first_name, self.last_name] if x)

    def full_name_de(self):
        return " ".join(x.strip() for x in [self.title_de, self.first_name_de, self.last_name_de] if x)

    def full_name_cz(self):
        return " ".join(x.strip() for x in [self.title_cz, self.first_name_cz, self.last_name_cz] if x)

    def __str__(self):
        return " ".join(x.strip() for x in [self.i18n_title, self.i18n_first_name, self.i18n_last_name] if x)

    class Meta:
        abstract = True


class I18nPage(Page):
    """
    An abstract base page class that supports translated content.
    """

    title_de = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        help_text=_("The page title as you'd like it to be seen by the public")
    )
    title_cz = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        help_text=_("The page title as you'd like it to be seen by the public")
    )
    draft_title_de = models.CharField(
        max_length=255,
        editable=False
    )
    draft_title_cz = models.CharField(
        max_length=255,
        editable=False
    )

    i18n_title = TranslatedField("title", "title_de", "title_cz")
    i18n_draft_title = TranslatedField("draft_title", "draft_title_de", "draft_title_cz")

    search_fields = Page.search_fields + [
        index.SearchField("title_de"),
        index.SearchField("title_cz"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("title_de"),
        FieldPanel("title_cz"),
    ]

    is_creatable = True

    def get_admin_display_title(self):
        return self.i18n_draft_title or self.i18n_title

    def full_clean(self, *args, **kwargs):
        if not self.draft_title_de:
            self.draft_title_de = self.title_de
        if not self.draft_title_cz:
            self.draft_title_cz = self.title_cz

        super(I18nPage, self).full_clean(*args, **kwargs)

    def save_revision(self, user=None, submitted_for_moderation=False, approved_go_live_at=None, changed=True):
        self.full_clean()

        # Create revision
        revision = self.revisions.create(
            content_json=self.to_json(),
            user=user,
            submitted_for_moderation=submitted_for_moderation,
            approved_go_live_at=approved_go_live_at,
        )

        update_fields = []

        self.latest_revision_created_at = revision.created_at
        update_fields.append('latest_revision_created_at')

        self.draft_title = self.title
        self.draft_title_de = self.title_de
        self.draft_title_cz = self.title_cz
        update_fields.append("draft_title")
        update_fields.append("draft_title_de")
        update_fields.append("draft_title_cz")

        if changed:
            self.has_unpublished_changes = True
            update_fields.append('has_unpublished_changes')

        if update_fields:
            self.save(update_fields=update_fields)

        # Log
        logger.info("Page edited: \"%s\" id=%d revision_id=%d", self.title, self.id, revision.id)

        if submitted_for_moderation:
            logger.info("Page submitted for moderation: \"%s\" id=%d revision_id=%d", self.title, self.id, revision.id)

        return revision

    def __str__(self):
        return self.i18n_title


class HomePage(I18nPage):
    parent_page_types = ["wagtailcore.Page"]

    @classmethod
    def can_create_at(cls, parent):
        return super(HomePage, cls).can_create_at(parent) \
               and not cls.objects.exists()

    class Meta:
        proxy = True


class TextTypesPage(I18nPage):
    parent_page_types = ["HomePage"]

    @classmethod
    def can_create_at(cls, parent):
        return super(TextTypesPage, cls).can_create_at(parent) and not cls.objects.exists()

    class Meta:
        proxy = True


class TextTypePage(I18nPage):
    parent_page_types = ["TextTypesPage",]

    class Meta:
        verbose_name = _("Text type")
        verbose_name_plural = _("Text types")


class ContactTypesPage(I18nPage):
    parent_page_types = ["HomePage"]

    @classmethod
    def can_create_at(cls, parent):
        return super(ContactTypesPage, cls).can_create_at(parent) and not cls.objects.exists()

    class Meta:
        proxy = True


class ContactTypePage(I18nPage):
    parent_page_types = ["ContactTypesPage",]

    class Meta:
        verbose_name = _("Contact type")
        verbose_name_plural = _("Contact types")


class LiteraryPeriodsPage(I18nPage):
    parent_page_types = ["HomePage",]

    @classmethod
    def can_create_at(cls, parent):
        return super(LiteraryPeriodsPage, cls).can_create_at(parent) and not cls.objects.exists()

    class Meta:
        proxy = True


class LiteraryPeriodPage(I18nPage, Describable):
    parent_page_types = ["LiteraryPeriodsPage", "LiteraryPeriodPage",]

    content_panels = [
        FieldPanel("title"),
        FieldPanel("description"),
    ]
    content_panels_de = [
        FieldPanel("title_de"),
        FieldPanel("description_de"),
    ]
    content_panels_cz = [
        FieldPanel("title_cz"),
        FieldPanel("description_cz"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading=_("Content (EN)"), classname="i18n en"),
        ObjectList(content_panels_de, heading=_("Content (DE)"), classname="i18n de"),
        ObjectList(content_panels_cz, heading=_("Content (CZ)"), classname="i18n cz"),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


class LiteraryCategoriesPage(I18nPage):
    parent_page_types = ["HomePage"]

    @classmethod
    def can_create_at(cls, parent):
        return super(LiteraryCategoriesPage, cls).can_create_at(parent) and not cls.objects.exists()

    class Meta:
        proxy = True


class LiteraryCategoryPage(I18nPage):
    parent_page_types = ["LiteraryCategoriesPage", "LiteraryCategoryPage",]

    class Meta:
        verbose_name = _("Literary category")
        verbose_name_plural = _("Literary categories")


class AuthorsPage(I18nPage):
    parent_page_types = ["HomePage"]

    @classmethod
    def can_create_at(cls, parent):
        return super(AuthorsPage, cls).can_create_at(parent) and not cls.objects.exists()

    class Meta:
        proxy = True


class AuthorPage(I18nPage):
    date_of_birth = models.DateField(_("Date of birth"), null=True, blank=True)
    date_of_death = models.DateField(_("Date of death"), null=True, blank=True)

    content_panels = [
        InlinePanel("names", label=_("Names"), min_num=1, help_text=_("The name of the author.")),
        FieldPanel("date_of_birth"),
        FieldPanel("date_of_death"),
    ]

    parent_page_types = ["AuthorsPage"]

    search_fields = Page.search_fields + [
        index.RelatedFields("names", [
            index.SearchField("title"),
            index.SearchField("first_name"),
            index.SearchField("last_name"),
            index.FilterField("is_birth_name"),
            index.FilterField("is_pseudonym"),
        ]),
        index.FilterField("date_of_birth"),
        index.FilterField("date_of_death"),
    ]

    def __init__(self, *args, **kwargs):
        self._meta.get_field("slug").default = BLANK_TEXT
        super(AuthorPage, self).__init__(*args, **kwargs)

    def clean(self):
        if not self.title:
            self.title = BLANK_TEXT
        if not self.title_de:
            self.title_de = BLANK_TEXT
        if not self.title_cz:
            self.title_cz = BLANK_TEXT
        name = self.names.first()
        if name:
            print(name)
            self.title = name.full_name()
            self.title_de = name.full_name_de()
            self.title_cz = name.full_name_cz()
            self.slug = text.slugify(self.title)

    def get_context(self, request, *args, **kwargs):
        context = super(AuthorPage, self).get_context(request, *args, **kwargs)
        context["sub_pages"] = self.get_children().specific()
        context["memories"] = self.memories.specific()
        return context


class AuthorPageName(Orderable, Name):
    author = ParentalKey("AuthorPage", related_name="names")


class PoisPage(I18nPage):
    parent_page_types = ["HomePage"]

    @classmethod
    def can_create_at(cls, parent):
        return super(PoisPage, cls).can_create_at(parent) and not cls.objects.exists()

    class Meta:
        proxy = True


class PoiPage(I18nPage, Describable):
    address = models.TextField(blank=True)
    address_de = models.TextField(blank=True)
    address_cz = models.TextField(blank=True)
    i18n_address = TranslatedField("address", "address_de", "address_cz")

    directions = models.TextField()
    directions_de = models.TextField()
    directions_cz = models.TextField()
    i18n_directions = TranslatedField("directions", "directions_de", "directions_cz")

    location = PointField(null=True, blank=True)

    search_fields = I18nPage.search_fields + [
        index.SearchField("description"),
        index.SearchField("description_de"),
        index.SearchField("description_cz"),
        index.SearchField("directions"),
        index.SearchField("directions_de"),
        index.SearchField("directions_cz"),
    ]

    parent_page_types = ["PoisPage"]

    general_panels = [
        FieldPanel("location", widget=GooglePointFieldWidget()),
    ]
    content_panels = [
        FieldPanel("title", classname="full title"),
        FieldPanel("description"),
        FieldPanel("address"),
        FieldPanel("directions"),
    ]
    content_panels_de = [
        FieldPanel("title_de", classname="full title"),
        FieldPanel("description_de"),
        FieldPanel("address_de"),
        FieldPanel("directions_de"),
    ]
    content_panels_cz = [
        FieldPanel("title_cz", classname="full title"),
        FieldPanel("description_cz"),
        FieldPanel("address_cz"),
        FieldPanel("directions_cz"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(general_panels, heading=_("General")),
        ObjectList(content_panels, heading=_("Content (EN)"), classname="i18n en"),
        ObjectList(content_panels_de, heading=_("Content (DE)"), classname="i18n de"),
        ObjectList(content_panels_cz, heading=_("Content (CZ)"), classname="i18n cz"),
    ])

    def __str__(self):
        return self.i18n_title


class MemoryPage(I18nPage):
    author = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="memories"
    )

    parent_page_types = ["PoiPage"]

    content_panels = [
        PageChooserPanel("author", "home.AuthorPage"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading=_("General"))
    ])

    def clean(self):
        author = self.author.specific
        self.title = author.title
        self.title_de = author.title
        self.title_cz = author.title
        self.slug = text.slugify(self.title)

        super(MemoryPage, self).clean()


class ContentPage(I18nPage):
    level = models.CharField(max_length=12, choices=LEVEL_CHOICES)
    body = StreamField([
        ("heading", blocks.PageChooserBlock(target_model="home.TextTypePage")),
        ("paragraph", blocks.RichTextBlock(features=["bold", "italic", "ol", "ul", "document-link"])),
        ("quote", blocks.BlockQuoteBlock()),
        ("image", ImageChooserBlock()),
        ("gallery", blocks.ListBlock(ImageChooserBlock(label=_("Image")))),
    ])
    body_de = StreamField([
        ("heading", blocks.PageChooserBlock(target_model="home.TextTypePage")),
        ("paragraph", blocks.RichTextBlock(features=["bold", "italic", "ol", "ul", "document-link"])),
        ("quote", blocks.BlockQuoteBlock()),
        ("image", ImageChooserBlock()),
        ("gallery", blocks.ListBlock(ImageChooserBlock(label=_("Image")))),
    ])
    body_cz = StreamField([
        ("heading", blocks.PageChooserBlock(target_model="home.TextTypePage")),
        ("paragraph", blocks.RichTextBlock(features=["bold", "italic", "ol", "ul", "document-link"])),
        ("quote", blocks.BlockQuoteBlock()),
        ("image", ImageChooserBlock()),
        ("gallery", blocks.ListBlock(ImageChooserBlock(label=_("Image")))),
    ])

    i18n_body = TranslatedField("body", "body_de", "body_cz")

    is_creatable = False
    parent_page_types = ["AuthorPage", "MemoryPage"]

    search_fields = I18nPage.search_fields + [
        index.SearchField("body"),
        index.SearchField("body_de"),
        index.SearchField("body_cz"),
    ]

    content_panels = [
        StreamFieldPanel("body"),
    ]
    content_panels_de = [
        StreamFieldPanel("body_de"),
    ]
    content_panels_cz = [
        StreamFieldPanel("body_cz"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading=_("Content (EN)"), classname="i18n en"),
        ObjectList(content_panels_de, heading=_("Content (DE)"), classname="i18n de"),
        ObjectList(content_panels_cz, heading=_("Content (CZ)"), classname="i18n cz"),
    ])

    def clean(self):
        self.title = self.get_level_display()
        self.title_de = self.get_level_display()
        self.title_cz = self.get_level_display()
        self.slug = text.slugify(self.title)

        super(ContentPage, self).clean()


class DiscoverContentPage(ContentPage):

    is_creatable = True

    def __init__(self, *args, **kwargs):
        self._meta.get_field("level").default = LEVEL_DISCOVER
        super(DiscoverContentPage, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = _("I. Discover")


class DeepenContentPage(ContentPage):

    is_creatable = True

    def __init__(self, *args, **kwargs):
        self._meta.get_field("level").default = LEVEL_DISCOVER
        super(DeepenContentPage, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = _("II. Deepen")


class ResearchContentPage(ContentPage):

    is_creatable = True

    def __init__(self, *args, **kwargs):
        self._meta.get_field("level").default = LEVEL_DISCOVER
        super(ResearchContentPage, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = _("III. Research")
