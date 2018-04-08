import logging

import datetime
from django.contrib.gis.db.models import PointField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import text, translation, dates
from django.utils.translation import ugettext_lazy as _
from mapwidgets import GooglePointFieldWidget
from modelcluster.fields import ParentalKey
from wagtail.core import blocks
from wagtail.core.fields import StreamField

from wagtail.core.models import Orderable, Page
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, TabbedInterface, ObjectList, StreamFieldPanel, \
    PageChooserPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import AbstractImage, AbstractRendition
from wagtail.search import index

logger = logging.getLogger('wagtail.core')

BLANK_TEXT = "_blank"


def validate_date(year=None, month=None, day=None):
    if year and month and day:
        datetime.datetime(year, month, day)
    elif month == 2 and day > 29:
        raise ValueError(_("February can't have more than 29 days."))
    elif not month % 2 and day > 30:
        raise ValueError(_("Day is out of range for month."))


class TranslatedField(object):
    """
    Helper class to add a getter method returning multilingual field content in the current selected user language.
    """

    def __init__(self, en_field, de_field, cz_field):
        self.en_field = en_field
        self.de_field = de_field
        self.cz_field = cz_field

    def __get__(self, instance, owner):
        lang = translation.get_language()
        if lang == "de":
            return getattr(instance, self.de_field) or getattr(instance, self.en_field)
        if lang == "cz":
            return getattr(instance, self.cz_field) or getattr(instance, self.en_field)
        else:
            return getattr(instance, self.en_field)


class ImageMedia(AbstractImage):
    title_de = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name=_("Title (de)")
    )
    title_cz = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name=_("Title (cz)")
    )
    i18n_title = TranslatedField("title", "title_de", "title_cz")

    alt_title = models.CharField(
        max_length=1024,
        null=True, blank=True,
        verbose_name=_("Alternative title")
    )
    alt_title_de = models.CharField(
        max_length=1024,
        null=True, blank=True,
        verbose_name=_("Alternative title (de)")
    )
    alt_title_cz = models.CharField(
        max_length=1024,
        null=True, blank=True,
        verbose_name=_("Alternative title (cz)")
    )
    i18n_alt_title = TranslatedField("alt_title", "alt_title_de", "alt_title_cz")

    admin_form_fields = (
        "title",
        "title_de",
        "title_cz",
        "file",
        "collection",
        "alt_title",
        "alt_title_de",
        "alt_title_cz",
        "tags",
        "focal_point_x",
        "focal_point_y",
        "focal_point_width",
        "focal_point_height",
    )

    def __str__(self):
        return self.i18n_title

    class Meta:
        db_table = "image"


class ImageMediaRendition(AbstractRendition):
    image = models.ForeignKey(ImageMedia, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        db_table = "image_rendition"
        unique_together = (
            ("image", "filter_spec", "focal_point_key"),
        )


class Name(models.Model):
    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Title")
    )
    title_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Title")
    )
    title_cz = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Title")
    )
    i18n_title = TranslatedField("title", "title_de", "title_cz")

    first_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("First name")
    )
    first_name_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("First name")
    )
    first_name_cz = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("First name")
    )
    i18n_first_name = TranslatedField("first_name", "first_name_de", "first_name_cz")

    last_name = models.CharField(
        max_length=255,
        verbose_name=_("Last name")
    )
    last_name_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Last name")
    )
    last_name_cz = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Last name")
    )
    i18n_last_name = TranslatedField("last_name", "last_name_de", "last_name_cz")

    birth_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Birth name")
    )
    birth_name_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Birth name")
    )
    birth_name_cz = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Birth name")
    )
    i18n_birth_name = TranslatedField("birth_name", "birth_name_de", "birth_name_cz")

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
        blank=True,
        help_text=_("The page title as you'd like it to be seen by the public")
    )
    title_cz = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        blank=True,
        help_text=_("The page title as you'd like it to be seen by the public")
    )
    draft_title_de = models.CharField(
        max_length=255,
        blank=True,
        editable=False
    )
    draft_title_cz = models.CharField(
        max_length=255,
        blank=True,
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

    is_creatable = False

    def __init__(self, *args, **kwargs):
        self._meta.get_field("slug").default = BLANK_TEXT
        super(I18nPage, self).__init__(*args, **kwargs)

    def get_admin_display_title(self):
        return self.i18n_draft_title or self.i18n_title

    def clean(self):
        super(I18nPage, self).clean()
        if not self.slug or self.slug == BLANK_TEXT:
            self.slug = text.slugify(self.title)

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


class CategoryPage(I18nPage):
    """
    A simple category page with a multilingual title field that can only be created once at the root level of the CMS.
    """

    @classmethod
    def can_create_at(cls, parent):
        return super(CategoryPage, cls).can_create_at(parent) and not cls.objects.exists()

    class Meta:
        abstract = True


class HomePage(CategoryPage):
    """
    The root page of the LIS cms site.
    """
    parent_page_types = ["wagtailcore.Page"]

    class Meta:
        verbose_name = _("Homepage")
        db_table = "homepage"


class LiteraryCategoriesPage(CategoryPage):
    parent_page_types = ["HomePage"]

    class Meta:
        verbose_name = _("Literary categories")
        db_table = "literary_categories"


class LiteraryCategoryPage(I18nPage):
    parent_page_types = ["LiteraryCategoriesPage"]

    class Meta:
        verbose_name = _("Literary category")
        verbose_name_plural = _("Literary categories")
        db_table = "literary_category"


class TextTypesPage(CategoryPage):
    parent_page_types = ["cms.HomePage"]

    class Meta:
        verbose_name = _("Text types")
        db_table = "text_types"


class TextTypePage(I18nPage):
    parent_page_types = ["TextTypesPage"]

    class Meta:
        verbose_name = _("Text type")
        verbose_name_plural = _("Text types")
        db_table = "text_type"


class ContactTypesPage(CategoryPage):
    parent_page_types = ["HomePage"]

    class Meta:
        verbose_name = _("Contact types")
        db_table = "contact_types"


class ContactTypePage(I18nPage):
    parent_page_types = ["ContactTypesPage"]

    class Meta:
        verbose_name = _("Contact type")
        verbose_name_plural = _("Contact types")
        db_table = "contact_type"


class LiteraryPeriodsPage(CategoryPage):
    parent_page_types = ["HomePage"]

    class Meta:
        verbose_name = _("Literary periods")
        db_table = "literary_periods"


class LiteraryPeriodPage(I18nPage):
    description = models.TextField(blank=True)
    description_de = models.TextField(blank=True)
    description_cz = models.TextField(blank=True)
    i18n_description = TranslatedField("description", "description_de", "description_cz")

    parent_page_types = ["LiteraryPeriodsPage", "LiteraryPeriodPage"]

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


class AuthorsPage(CategoryPage):
    parent_page_types = ["HomePage"]

    class Meta:
        verbose_name = _("Authors")
        db_table = "authors"


class AuthorPage(I18nPage):
    SEX_UNKNOWN = "U"
    SEX_MALE = "M"
    SEX_FEMALE = "F"
    SEX_CHOICES = (
        (SEX_UNKNOWN, _("Unknown")),
        (SEX_MALE, _("Male")),
        (SEX_FEMALE, _("Female")),
    )

    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default=SEX_UNKNOWN)
    date_of_birth_year = models.PositiveSmallIntegerField(
        _("Year of birth"),
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(9999)]
    )
    date_of_birth_month = models.PositiveSmallIntegerField(
        _("Month of birth"),
        choices=dates.MONTHS.items(),
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    date_of_birth_day = models.PositiveSmallIntegerField(
        _("Day of birth"),
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)]
    )
    date_of_death_year = models.PositiveSmallIntegerField(
        _("Year of death"),
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(9999)]
    )
    date_of_death_month = models.PositiveSmallIntegerField(
        _("Month of death"),
        choices=dates.MONTHS.items(),
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    date_of_death_day = models.PositiveSmallIntegerField(
        _("Day of death"),
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)]
    )

    content_panels = [
        InlinePanel(
            "names",
            panels=[
                MultiFieldPanel(
                    children=[
                        FieldPanel("title"),
                        FieldPanel("first_name"),
                        FieldPanel("last_name"),
                        FieldPanel("birth_name"),
                    ],
                    heading=_("English"),
                    classname="collapsible"
                ),
                MultiFieldPanel(
                    children=[
                        FieldPanel("title_de"),
                        FieldPanel("first_name_de"),
                        FieldPanel("last_name_de"),
                        FieldPanel("birth_name_de"),
                    ],
                    heading=_("German")
                ),
                MultiFieldPanel(
                    children=[
                        FieldPanel("title_cz"),
                        FieldPanel("first_name_cz"),
                        FieldPanel("last_name_cz"),
                        FieldPanel("birth_name_cz"),
                    ],
                    heading=_("Czech")
                ),
                FieldPanel("is_pseudonym"),
            ],
            label=_("Names"),
            min_num=1,
            help_text=_("The name of the author.")
        ),
        FieldPanel("sex"),
        MultiFieldPanel(
            children=[
                FieldPanel("date_of_birth_day"),
                FieldPanel("date_of_birth_month"),
                FieldPanel("date_of_birth_year")
            ],
            heading=_("Date of birth")
        ),
        MultiFieldPanel(
            children=[
                FieldPanel("date_of_death_day"),
                FieldPanel("date_of_death_month"),
                FieldPanel("date_of_death_year")
            ],
            heading=_("Date of death")
        ),
        InlinePanel(
            "literary_periods",
            label=_("Literary periods"),
            min_num=0,
            help_text=_("The literary periods the author has been active in.")
        ),
        InlinePanel(
            "literary_categories",
            label=_("Literary categories"),
            min_num=0,
            help_text=_("The literary categories the author is associated with.")
        )
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
        index.FilterField("date_of_birth_year"),
        index.FilterField("date_of_death_year"),
    ]

    edit_handler = ObjectList(content_panels, heading=_("Content (EN)"))

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
            self.title = name.full_name()
            self.title_de = name.full_name_de()
            self.title_cz = name.full_name_cz()
            self.slug = text.slugify(self.title)

        validate_date(self.date_of_birth_year, self.date_of_birth_month, self.date_of_birth_day)
        validate_date(self.date_of_death_year, self.date_of_death_month, self.date_of_death_day)

    def get_context(self, request, *args, **kwargs):
        context = super(AuthorPage, self).get_context(request, *args, **kwargs)
        context["sub_pages"] = self.get_children().specific()
        context["memories"] = self.memories.specific()
        return context

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")


class AuthorPageName(Orderable, Name):
    author = ParentalKey("AuthorPage", related_name="names")


class AuthorLiteraryPeriod(Orderable):
    author = ParentalKey("AuthorPage", related_name="literary_periods")
    literary_period = models.ForeignKey(
        LiteraryPeriodPage,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="authors"
    )

    class Meta:
        db_table = "author_literary_period"


class AuthorLiteraryCategory(Orderable):
    author = ParentalKey("AuthorPage", related_name="literary_categories")
    literary_category = models.ForeignKey(
        LiteraryCategoryPage,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="authors"
    )

    class Meta:
        db_table = "author_literary_category"


class LocationTypesPage(CategoryPage):
    parent_page_types = ["HomePage"]

    class Meta:
        verbose_name = _("Location types")
        db_table = "location_types"


class LocationTypePage(I18nPage):
    parent_page_types = ["LocationTypesPage"]

    class Meta:
        verbose_name = _("Location type")
        verbose_name_plural = _("Location types")
        db_table = "location_type"


class LocationsPage(CategoryPage):
    parent_page_types = ["HomePage"]

    class Meta:
        verbose_name = _("Locations")
        db_table = "locations"


class LocationPage(I18nPage):
    location_type = models.ForeignKey(
        "LocationTypePage",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="locations"
    )

    description = models.TextField(blank=True)
    description_de = models.TextField(blank=True)
    description_cz = models.TextField(blank=True)
    i18n_description = TranslatedField("description", "description_de", "description_cz")

    address = models.TextField(blank=True)
    address_de = models.TextField(blank=True)
    address_cz = models.TextField(blank=True)
    i18n_address = TranslatedField("address", "address_de", "address_cz")

    directions = models.TextField(blank=True)
    directions_de = models.TextField(blank=True)
    directions_cz = models.TextField(blank=True)
    i18n_directions = TranslatedField("directions", "directions_de", "directions_cz")

    coordinates = PointField(null=True, blank=True)

    search_fields = I18nPage.search_fields + [
        index.SearchField("description"),
        index.SearchField("description_de"),
        index.SearchField("description_cz"),
        index.SearchField("directions"),
        index.SearchField("directions_de"),
        index.SearchField("directions_cz"),
    ]

    parent_page_types = ["LocationsPage"]

    general_panels = [
        PageChooserPanel("location_type", "cms.LocationTypePage"),
        FieldPanel("coordinates", widget=GooglePointFieldWidget()),
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

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        db_table = "location"


class MemorialSitePage(I18nPage):
    author = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="memories"
    )

    parent_page_types = ["LocationPage"]

    content_panels = [
        PageChooserPanel("author", "cms.AuthorPage"),
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

        super(MemorialSitePage, self).clean()

    class Meta:
        verbose_name = _("Memorial site")
        verbose_name_plural = _("Memorial sites")
        db_table = "mermorial_site"


class HeadingWithContentPage(I18nPage):
    LEVEL_DISCOVER = "I"
    LEVEL_DEEPEN = "II"
    LEVEL_RESEARCH = "III"
    LEVEL_CHOICES = (
        (LEVEL_DISCOVER, _("I. Discover")),
        (LEVEL_DEEPEN, _("II. Deepen")),
        (LEVEL_RESEARCH, _("III. Research")),
    )

    level = models.CharField(max_length=12, choices=LEVEL_CHOICES)
    body = StreamField(
        block_types=[
            ("heading", blocks.PageChooserBlock(target_model="cms.TextTypePage")),
            ("paragraph", blocks.RichTextBlock(
                features=[
                    "bold",
                    "italic",
                    "strikethrough",
                    "sup",
                    "ol",
                    "ul",
                    "hr",
                    "blockquote"
                ]
            )),
            ("quote", blocks.BlockQuoteBlock()),
            ("image", ImageChooserBlock()),
            ("gallery", blocks.ListBlock(ImageChooserBlock(label=_("Image")))),
        ],
        blank=True
    )
    body_de = StreamField(
        block_types=[
            ("heading", blocks.PageChooserBlock(target_model="cms.TextTypePage")),
            ("paragraph", blocks.RichTextBlock(features=["bold", "italic", "ol", "ul", "document-link"])),
            ("quote", blocks.BlockQuoteBlock()),
            ("image", ImageChooserBlock()),
            ("gallery", blocks.ListBlock(ImageChooserBlock(label=_("Image")))),
        ],
        blank=True
    )
    body_cz = StreamField(
        block_types=[
            ("heading", blocks.PageChooserBlock(target_model="cms.TextTypePage")),
            ("paragraph", blocks.RichTextBlock(features=["bold", "italic", "ol", "ul", "document-link"])),
            ("quote", blocks.BlockQuoteBlock()),
            ("image", ImageChooserBlock()),
            ("gallery", blocks.ListBlock(ImageChooserBlock(label=_("Image")))),
        ],
        blank=True
    )

    i18n_body = TranslatedField("body", "body_de", "body_cz")

    is_creatable = False
    parent_page_types = ["AuthorPage", "MemorialSitePage"]

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
        super(HeadingWithContentPage, self).clean()

    class Meta:
        abstract = True


class DiscoverPage(HeadingWithContentPage):

    def __init__(self, *args, **kwargs):
        self._meta.get_field("level").default = HeadingWithContentPage.LEVEL_DISCOVER
        super(DiscoverPage, self).__init__(*args, **kwargs)

    class Meta:
        verbose_name = _("I. Discover")


class DeepenPage(HeadingWithContentPage):

    def __init__(self, *args, **kwargs):
        self._meta.get_field("level").default = HeadingWithContentPage.LEVEL_DEEPEN
        super(DeepenPage, self).__init__(*args, **kwargs)

    class Meta:
        verbose_name = _("II. Deepen")


class ResearchPage(HeadingWithContentPage):

    def __init__(self, *args, **kwargs):
        self._meta.get_field("level").default = HeadingWithContentPage.LEVEL_RESEARCH
        super(ResearchPage, self).__init__(*args, **kwargs)

    class Meta:
        verbose_name = _("III. Research")
