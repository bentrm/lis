"""Custom page models that describe the LIS data schema."""

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

from wagtail.core.models import Orderable, Page, CollectionMember
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, TabbedInterface, ObjectList, \
    PageChooserPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.documents.models import AbstractDocument
from wagtail.images.models import AbstractImage, AbstractRendition
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from .blocks import ParagraphStructBlock

logger = logging.getLogger('wagtail.core')

BLANK_TEXT = "_blank"
EDITOR_FEATURES = [
    "bold",
    "italic",
    "strikethrough",
    "sup",
    "ol",
    "ul",
    "hr",
    "blockquote",
    "link"]


def validate_date(year=None, month=None, day=None):
    """Validate a given date for semantic integrity."""
    if year and month and day:
        datetime.datetime(year, month, day)
    elif month and day:
        if month == 2 and day > 29:
            raise ValueError(_("February can't have more than 29 days."))
        elif not month % 2 and day > 30:
            raise ValueError(_("Day is out of range for month."))


class TranslatedField(object):
    """Helper class to add multilingual accessor properties to user content."""

    def __init__(self, en_field, de_field, cs_field):
        self.en_field = en_field
        self.de_field = de_field
        self.cs_field = cs_field

    def __get__(self, instance, owner):
        lang = translation.get_language()
        default_value = getattr(instance, self.en_field) or ""
        if lang == "de":
            return getattr(instance, self.de_field) or default_value
        if lang == "cs":
            return getattr(instance, self.cs_field) or default_value
        return default_value


class Media(models.Model):
    """Implements the basic Media interface that will be used by custom media classes like images and documents."""

    title_de = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name=_("Title (de)")
    )
    title_cs = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name=_("Title (cz)")
    )
    i18n_title = TranslatedField("title", "title_de", "title_cs")

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
    alt_title_cs = models.CharField(
        max_length=1024,
        null=True, blank=True,
        verbose_name=_("Alternative title (cz)")
    )
    i18n_alt_title = TranslatedField("alt_title", "alt_title_de", "alt_title_cs")

    caption = models.CharField(
        max_length=1024,
        null=True, blank=True,
        verbose_name=_("Media caption")
    )
    caption_de = models.CharField(
        max_length=1024,
        null=True, blank=True,
        verbose_name=_("Media caption (de)")
    )
    caption_cs = models.CharField(
        max_length=1024,
        null=True, blank=True,
        verbose_name=_("Media caption (cz)")
    )
    i18n_caption = TranslatedField("caption", "caption_de", "caption_cs")

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
        index.SearchField('alt_title', partial_match=True, boost=5),
        index.FilterField('alt_title'),
        index.SearchField('alt_title_de', partial_match=True, boost=5),
        index.FilterField('alt_title_de'),
        index.SearchField('alt_title_cs', partial_match=True, boost=5),
        index.FilterField('alt_title_cs'),
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
        return self.i18n_title

    class Meta:
        abstract = True


class ImageMedia(Media, AbstractImage):
    """Custom image implementation to add meta data properties as described by the LIS data schema."""

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

    image = models.ForeignKey(ImageMedia, on_delete=models.CASCADE, related_name='renditions')

    @property
    def alt(self):
        """Return the alternative title in the current selected user language."""
        return self.image.i18n_alt_title

    class Meta:
        db_table = "image_rendition"
        unique_together = (
            ("image", "filter_spec", "focal_point_key"),
        )


class DocumentMedia(Media, AbstractDocument):
    """Custom document implementation to add meta data properties as described by the LIS data schema."""

    class Meta:
        db_table = "document"


class I18nPage(Page):
    """An abstract base page class that supports translated content."""

    title_de = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        blank=True,
        help_text=_("The page title as you'd like it to be seen by the public"))
    title_cs = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        blank=True,
        help_text=_("The page title as you'd like it to be seen by the public"))
    i18n_title = TranslatedField("title", "title_de", "title_cs")

    draft_title_de = models.CharField(
        max_length=255,
        blank=True,
        editable=False)
    draft_title_cs = models.CharField(
        max_length=255,
        blank=True,
        editable=False)
    i18n_draft_title = TranslatedField("draft_title", "draft_title_de", "draft_title_cs")

    editor = models.CharField(
        max_length=2048,
        verbose_name=_("Editor"),
        help_text=_("Name of the author of this content."))

    search_fields = Page.search_fields + [
        index.SearchField('title_de', partial_match=True, boost=2),
        index.SearchField('title_cs', partial_match=True, boost=2)]

    content_panels = [
        FieldPanel("title", classname="full title"),
        FieldPanel("title_de", classname="full title"),
        FieldPanel("title_cs", classname="full title")]

    meta_panels = [
        FieldPanel("owner"),
        FieldPanel("editor")]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading=_("Content")),
        ObjectList(meta_panels, heading=_("Meta"))])

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
        if not self.draft_title_cs:
            self.draft_title_cs = self.title_cs
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
        self.draft_title_cs = self.title_cs
        update_fields.append("draft_title")
        update_fields.append("draft_title_de")
        update_fields.append("draft_title_cs")

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
    description_cs = models.TextField(blank=True)
    i18n_description = TranslatedField("description", "description_de", "description_cs")

    parent_page_types = ["LiteraryPeriodsPage", "LiteraryPeriodPage"]

    content_panels = [
        FieldPanel("title"),
        FieldPanel("description"),
    ]
    content_panels_de = [
        FieldPanel("title_de"),
        FieldPanel("description_de"),
    ]
    content_panels_cs = [
        FieldPanel("title_cs"),
        FieldPanel("description_cs"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading=_("Content (EN)"), classname="i18n en"),
        ObjectList(content_panels_de, heading=_("Content (DE)"), classname="i18n de"),
        ObjectList(content_panels_cs, heading=_("Content (CZ)"), classname="i18n cz"),
        ObjectList(I18nPage.meta_panels, heading=_("Meta")),
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

    title_image = models.ForeignKey(
        ImageMedia,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
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
        ImageChooserPanel("title_image"),
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
                        FieldPanel("title_cs"),
                        FieldPanel("first_name_cs"),
                        FieldPanel("last_name_cs"),
                        FieldPanel("birth_name_cs"),
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
            help_text=_("The literary periods the author has been active in."),
            panels=[PageChooserPanel("literary_period", "cms.LiteraryPeriodPage")]
        ),
        InlinePanel(
            "literary_categories",
            label=_("Literary categories"),
            min_num=0,
            help_text=_("The literary categories the author is associated with."),
            panels=[PageChooserPanel("literary_category", "cms.LiteraryCategoryPage")]
        )
    ]

    parent_page_types = ["AuthorsPage"]

    search_fields = Page.search_fields + [
        index.RelatedFields("names", [
            index.SearchField("title"),
            index.SearchField("first_name"),
            index.SearchField("last_name"),
            index.FilterField("birth_name"),
            index.FilterField("is_pseudonym"),
        ]),
        index.FilterField("date_of_birth_year"),
        index.FilterField("date_of_death_year"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading=_("General")),
        ObjectList(I18nPage.meta_panels, heading=_("Meta"))])

    def __init__(self, *args, **kwargs):
        self._meta.get_field("slug").default = BLANK_TEXT
        super(AuthorPage, self).__init__(*args, **kwargs)

    def clean(self):
        if not self.title:
            self.title = BLANK_TEXT
        if not self.title_de:
            self.title_de = BLANK_TEXT
        if not self.title_cs:
            self.title_cs = BLANK_TEXT
        name = self.names.first()
        if name:
            self.title = name.full_name()
            self.title_de = name.full_name_de()
            self.title_cs = name.full_name_cs()
            self.slug = text.slugify(self.title)

        validate_date(self.date_of_birth_year, self.date_of_birth_month, self.date_of_birth_day)
        validate_date(self.date_of_death_year, self.date_of_death_month, self.date_of_death_day)

    def get_context(self, request, *args, **kwargs):
        context = super(AuthorPage, self).get_context(request, *args, **kwargs)
        context["sub_pages"] = self.get_children().specific()
        # context["memorial_sites"] = self.memorial_sites.all().specific()
        return context

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")


class AuthorPageName(Orderable):
    author = ParentalKey("AuthorPage", related_name="names")

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
    title_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Title")
    )
    i18n_title = TranslatedField("title", "title_de", "title_cs")

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
    first_name_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("First name")
    )
    i18n_first_name = TranslatedField("first_name", "first_name_de", "first_name_cs")

    last_name = models.CharField(
        max_length=255,
        verbose_name=_("Last name")
    )
    last_name_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Last name")
    )
    last_name_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Last name")
    )
    i18n_last_name = TranslatedField("last_name", "last_name_de", "last_name_cs")

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
    birth_name_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Birth name")
    )
    i18n_birth_name = TranslatedField("birth_name", "birth_name_de", "birth_name_cs")

    is_pseudonym = models.BooleanField(default=False)

    def clean(self):
        super(AuthorPageName, self).clean()
        if not self.first_name and not self.last_name:
            raise ValidationError(_("Name entries must at least define a first name or a last name."))

    def full_name(self):
        """Return the full name of the author in english language."""
        return " ".join(x.strip() for x in [self.title, self.first_name, self.last_name] if x)

    def full_name_de(self):
        """Return the full name of the author in german language."""
        return " ".join(x.strip() for x in [self.title_de, self.first_name_de, self.last_name_de] if x)

    def full_name_cs(self):
        """Return the full name of the author in czech language."""
        return " ".join(x.strip() for x in [self.title_cs, self.first_name_cs, self.last_name_cs] if x)

    def __str__(self):
        """Return the full name of the author in the current session language."""
        return " ".join(x.strip() for x in [self.i18n_title, self.i18n_first_name, self.i18n_last_name] if x)


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


class Level1Page(I18nPage):
    parent_page_types = ["AuthorPage"]

    TEXT_TYPES = (
        ("i18n_biography", _("Biography")),
        ("i18n_works", _("Works")))

    biography = StreamField([(_("Paragraph"), ParagraphStructBlock())], blank=True)
    biography_de = StreamField([(_("Paragraph"), ParagraphStructBlock())], blank=True)
    biography_cs = StreamField([(_("Paragraph"), ParagraphStructBlock())], blank=True)
    i18n_biography = TranslatedField("biography", "biography_de", "biography_cs")

    works = StreamField([(_("Paragraph"), ParagraphStructBlock())], blank=True)
    works_de = StreamField([(_("Paragraph"), ParagraphStructBlock())], blank=True)
    works_cs = StreamField([(_("Paragraph"), ParagraphStructBlock())], blank=True)
    i18n_works = TranslatedField("works", "works_de", "works_cs")

    default_panels = [
        FieldPanel("title", classname="full title"),
        StreamFieldPanel("biography", ),
        StreamFieldPanel("works", )]
    german_panels = [
        FieldPanel("title_de", classname="full title"),
        StreamFieldPanel("biography_de", ),
        StreamFieldPanel("works_de", )]
    czech_panels = [
        FieldPanel("title_cs", classname="full title"),
        StreamFieldPanel("biography_cs", ),
        StreamFieldPanel("works_cs", )]
    edit_handler = TabbedInterface([
        ObjectList(default_panels, heading=_("English"), classname="i18n en"),
        ObjectList(german_panels, heading=_("German"), classname="i18n de"),
        ObjectList(czech_panels, heading=_("Czech"), classname="i18n cz"),
        ObjectList(I18nPage.meta_panels, heading=_("Meta"))])

    @classmethod
    def can_create_at(cls, parent):
        """Determine the valid location of the page in the page hierarchy."""
        return super(Level1Page, cls).can_create_at(parent) and not cls.objects.exists()

    def __init__(self, *args, **kwargs):
        self._meta.get_field('title').default = "Discover"
        self._meta.get_field('title_de').default = "Entdecken"
        self._meta.get_field('title_cs').default = "Discover*"
        super(Level1Page, self).__init__(*args, **kwargs)

    def __str__(self):
        return f"I. {self.i18n_title}"

    class Meta:
        db_table = "level_1"
        verbose_name = _("I. Discover page")


class Level2Page(I18nPage):
    parent_page_types = ["AuthorPage"]

    perception = StreamField([(_("Paragraph"), ParagraphStructBlock())], blank=True)
    perception_de = StreamField([(_("Paragraph"), ParagraphStructBlock())], blank=True)
    perception_cs = StreamField([(_("Paragraph"), ParagraphStructBlock())], blank=True)
    i18n_perception = TranslatedField("perception", "perception_de", "perception_cs")

    default_panels = Level1Page.default_panels + [
        FieldPanel("perception")]
    german_panels = Level1Page.german_panels + [
        FieldPanel("perception_de")]
    czech_panels = Level1Page.czech_panels + [
        FieldPanel("perception_cs")]

    @classmethod
    def can_create_at(cls, parent):
        """Determine the valid location of the page in the page hierarchy."""
        return super(Level2Page, cls).can_create_at(parent) and not cls.objects.exists()

    def __init__(self, *args, **kwargs):
        self._meta.get_field('title').default = "Deepen"
        self._meta.get_field('title_de').default = "Vertiefen"
        self._meta.get_field('title_cs').default = "Deepen*"
        super(Level2Page, self).__init__(*args, **kwargs)

    def __str__(self):
        return f"II. {self.i18n_title}"

    class Meta:
        db_table = "level_2"
        verbose_name = _("II. Deepen page")


class Level3Page(I18nPage):
    parent_page_types = ["AuthorPage"]

    primary_literature = StreamField([(_("Paragraph"), ParagraphStructBlock())], blank=True)
    primary_literature_de = StreamField([(_("Paragraph"), ParagraphStructBlock())], blank=True)
    primary_literature_cs = StreamField([(_("Paragraph"), ParagraphStructBlock())], blank=True)
    i18n_primary_literature = TranslatedField("primary_literature", "primary_literature_de", "primary_literature_cs")

    testimony = StreamField([(_("Paragraph"), ParagraphStructBlock())], blank=True)
    testimony_de = StreamField([(_("Paragraph"), ParagraphStructBlock())], blank=True)
    testimony_cs = StreamField([(_("Paragraph"), ParagraphStructBlock())], blank=True)
    i18n_testimony = TranslatedField("testimony", "testimony_de", "testimony_cs")

    secondary_literature = StreamField([(_("Paragraph"), ParagraphStructBlock())], blank=True)
    secondary_literature_de = StreamField([(_("Paragraph"), ParagraphStructBlock())], blank=True)
    secondary_literature_cs = StreamField([(_("Paragraph"), ParagraphStructBlock())], blank=True)
    i18n_secondary_literature = TranslatedField(
        "secondary_literature",
        "secondary_literature_de",
        "secondary_literature_cs")

    default_panels = [
        FieldPanel("title", classname="full title"),
        StreamFieldPanel("primary_literature", ),
        StreamFieldPanel("testimony", ),
        StreamFieldPanel("secondary_literature", )]
    german_panels = [
        FieldPanel("title_de", classname="full title"),
        StreamFieldPanel("primary_literature_de", ),
        StreamFieldPanel("testimony_de", ),
        StreamFieldPanel("secondary_literature_de", )]
    czech_panels = [
        FieldPanel("title_cs", classname="full title"),
        StreamFieldPanel("primary_literature_cs", ),
        StreamFieldPanel("testimony_cs", ),
        StreamFieldPanel("secondary_literature_cs", )]
    edit_handler = TabbedInterface([
        ObjectList(default_panels, heading=_("English"), classname="i18n en"),
        ObjectList(german_panels, heading=_("German"), classname="i18n de"),
        ObjectList(czech_panels, heading=_("Czech"), classname="i18n cz"),
        ObjectList(I18nPage.meta_panels, heading=_("Meta"))])

    @classmethod
    def can_create_at(cls, parent):
        """Determine the valid location of the page in the page hierarchy."""
        return super(Level3Page, cls).can_create_at(parent) and not cls.objects.exists()

    def __init__(self, *args, **kwargs):
        self._meta.get_field('title').default = "Research"
        self._meta.get_field('title_de').default = "Forschen"
        self._meta.get_field('title_cs').default = "Research*"
        super(Level3Page, self).__init__(*args, **kwargs)

    def __str__(self):
        return f"III. {self.i18n_title}"

    class Meta:
        db_table = "level_3"
        verbose_name = _("III. Research page")


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
    title_image = models.ForeignKey(
        ImageMedia,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    location_type = models.ForeignKey(
        "LocationTypePage",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="locations"
    )

    description = models.TextField(blank=True)
    description_de = models.TextField(blank=True)
    description_cs = models.TextField(blank=True)
    i18n_description = TranslatedField("description", "description_de", "description_cs")

    address = models.TextField(blank=True)
    address_de = models.TextField(blank=True)
    address_cs = models.TextField(blank=True)
    i18n_address = TranslatedField("address", "address_de", "address_cs")

    directions = models.TextField(blank=True)
    directions_de = models.TextField(blank=True)
    directions_cs = models.TextField(blank=True)
    i18n_directions = TranslatedField("directions", "directions_de", "directions_cs")

    coordinates = PointField()

    search_fields = I18nPage.search_fields + [
        index.SearchField("description"),
        index.SearchField("description_de"),
        index.SearchField("description_cs"),
        index.SearchField("directions"),
        index.SearchField("directions_de"),
        index.SearchField("directions_cs"),
    ]

    parent_page_types = ["LocationsPage"]

    default_panels = [
        FieldPanel("title", classname="full title"),
        ImageChooserPanel("title_image"),
        PageChooserPanel("location_type", "cms.LocationTypePage"),
        InlinePanel(
            "contacts",
            label=_("Contacts"),
            min_num=0,
            panels=[
                PageChooserPanel("contact_type", "cms.ContactTypePage"),
                FieldPanel("name"),
                FieldPanel("name_de"),
                FieldPanel("name_cs")
            ],
            help_text=_("The authors that this memorial site is dedicated to.")),
        FieldPanel("description"),
        FieldPanel("address"),
        FieldPanel("directions"),
        FieldPanel("coordinates", widget=GooglePointFieldWidget()),
    ]
    german_panels = [
        FieldPanel("title_de", classname="full title"),
        FieldPanel("description_de"),
        FieldPanel("address_de"),
        FieldPanel("directions_de"),
    ]
    czech_panels = [
        FieldPanel("title_cs", classname="full title"),
        FieldPanel("description_cs"),
        FieldPanel("address_cs"),
        FieldPanel("directions_cs"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(default_panels, heading=_("English")),
        ObjectList(german_panels, heading=_("German"), classname="i18n en"),
        ObjectList(czech_panels, heading=_("Czech"), classname="i18n de"),
        ObjectList(I18nPage.meta_panels, heading=_("Meta")),
    ])

    def __str__(self):
        return self.i18n_title

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        db_table = "location"


class LocationPageContact(Orderable):
    location = ParentalKey("LocationPage", related_name="contacts")
    contact_type = models.ForeignKey(
        ContactTypePage,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="contacts"
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name (en)")
    )
    name_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Name (de)")
    )
    name_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Name (cs)")
    )
    i18n_name = TranslatedField("name", "name_de", "name_cs")


class MemorialSitePage(I18nPage):
    title_image = models.ForeignKey(
        ImageMedia,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    description = RichTextField(blank=True)
    description_de = RichTextField(blank=True)
    description_cs = RichTextField(blank=True)
    i18n_description = TranslatedField("description", "description_de", "description_cs")

    parent_page_types = ["LocationPage"]

    default_panels = [
        ImageChooserPanel("title_image"),
        InlinePanel(
            "authors",
            label=_("Authors"),
            min_num=0,
            help_text=_("The authors that this memorial site is dedicated to."),
            panels=[
                PageChooserPanel("author", "cms.AuthorPage")
            ]
        ),
        FieldPanel("description")
    ]

    german_panels = [
        FieldPanel("description_de")
    ]

    czech_panels = [
        FieldPanel("description_cs")
    ]

    edit_handler = TabbedInterface([
        ObjectList(default_panels, heading=_("English")),
        ObjectList(german_panels, heading=_("German")),
        ObjectList(czech_panels, heading=_("Czech")),
        ObjectList(I18nPage.meta_panels, heading=_("Meta")),
    ])

    def clean(self):
        """Clean page properties defaulting to the authors name of the memorial site."""

        super(MemorialSitePage, self).clean()

    def full_clean(self, *args, **kwargs):
        title = ", ".join([x.author.title for x in self.authors.all()])
        self.title = title
        self.slug = text.slugify(self.title)
        super(MemorialSitePage, self).full_clean(*args, **kwargs)

    def __str__(self):
        return _("Memorial site") + super(MemorialSitePage, self).__str__()

    class Meta:
        verbose_name = _("Memorial site")
        verbose_name_plural = _("Memorial sites")
        db_table = "mermorial_site"  # TODO: fix typo


class MemorialSiteAuthor(Orderable):
    """Join page type to add multiple authors to one memorial site."""

    memorial_site = ParentalKey("MemorialSitePage", related_name="authors")
    author = models.ForeignKey(
        AuthorPage,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="memorial_sites"
    )

    class Meta:
        db_table = "memorial_site_author"
