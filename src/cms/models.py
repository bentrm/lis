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
from wagtail.core.fields import StreamField
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
            raise ValueError(_("February cannot have more than 29 days."))
        elif not month % 2 and day > 30:
            raise ValueError(_("Day is out of range for the indicated month."))


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
        verbose_name=_("German title")
    )
    title_cs = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name=_("Czech title")
    )
    i18n_title = TranslatedField("title", "title_de", "title_cs")

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
        verbose_name=_("Caption"),
        help_text=_("A caption that may be presented with the file.")
    )
    caption_de = models.CharField(
        max_length=1024,
        null=True, blank=True,
        verbose_name=_("German caption"),
        help_text=_("Caption in German translations.")
    )
    caption_cs = models.CharField(
        max_length=1024,
        null=True, blank=True,
        verbose_name=_("Czech caption"),
        help_text=_("Caption in Czech translations.")
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

    image = models.ForeignKey(
        ImageMedia,
        on_delete=models.CASCADE,
        related_name="renditions",
        verbose_name=_("Image rendition"),
        help_text=_("The image this rendition is based on."))

    @property
    def alt(self):
        """Return the alternative title in the current selected user language."""
        return self.image.i18n_alt_title

    class Meta:
        db_table = "image_rendition"
        unique_together = (
            ("image", "filter_spec", "focal_point_key"))


class DocumentMedia(Media, AbstractDocument):
    """Custom document implementation to add meta data properties as described by the LIS data schema."""

    class Meta:
        db_table = "document"


class I18nPage(Page):
    """An abstract base page class that supports translated content."""

    ORIGINAL_LANGUAGE_ENGLISH = "en"
    ORIGINAL_LANGUAGE_GERMAN = "de"
    ORIGINAL_LANGUAGE_CZECH = "cs"
    ORIGINAL_LANGUAGE = (
        (ORIGINAL_LANGUAGE_ENGLISH, _("English")),
        (ORIGINAL_LANGUAGE_GERMAN, _("German")),
        (ORIGINAL_LANGUAGE_CZECH, _("Czech")))

    title_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("German title"),
        help_text=_("German title of the page."))
    title_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Czech title"),
        help_text=_("Czech title of the page."))
    i18n_title = TranslatedField("title", "title_de", "title_cs")

    draft_title_de = models.CharField(
        max_length=255,
        blank=True,
        editable=False,
        verbose_name=_("Draft title"),
        help_text=_("German title of the page as given in the latest draft."))
    draft_title_cs = models.CharField(
        max_length=255,
        blank=True,
        editable=False,
        verbose_name=_("Draft title"),
        help_text=_("Czech page title as given in the latest draft."))
    i18n_draft_title = TranslatedField("draft_title", "draft_title_de", "draft_title_cs")

    editor = models.CharField(
        max_length=2048,
        verbose_name=_("Editor"),
        help_text=_("Name or initials of the author of this content page."))
    original_language = models.CharField(
        max_length=3,
        choices=ORIGINAL_LANGUAGE,
        default=ORIGINAL_LANGUAGE_GERMAN,
        verbose_name=_("Original language"),
        help_text=_("The language this content has been originally written in."))

    search_fields = Page.search_fields + [
        index.SearchField('title_de', partial_match=True, boost=2),
        index.SearchField('title_cs', partial_match=True, boost=2)]

    content_panels = [
        FieldPanel("title", classname="full title"),
        FieldPanel("title_de", classname="full title"),
        FieldPanel("title_cs", classname="full title")]

    meta_panels = [
        FieldPanel("owner"),
        FieldPanel("editor"),
        FieldPanel("original_language")]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading=_("Content")),
        ObjectList(meta_panels, heading=_("Meta information"))])

    is_creatable = False

    def __init__(self, *args, **kwargs):
        self._meta.get_field("slug").default = BLANK_TEXT
        super(I18nPage, self).__init__(*args, **kwargs)

    def get_admin_display_title(self):
        """Return title to be displayed in the admins UI."""
        return self.i18n_draft_title or self.i18n_title

    def clean(self):
        """Add an autogenerated slug to the page derived from the title field."""
        super(I18nPage, self).clean()
        if not self.slug or self.slug == BLANK_TEXT:
            self.slug = text.slugify(self.title)

    def full_clean(self, *args, **kwargs):
        """Set the translated draft titles according the translated title fields."""
        if not self.draft_title_de:
            self.draft_title_de = self.title_de
        if not self.draft_title_cs:
            self.draft_title_cs = self.title_cs
        super(I18nPage, self).full_clean(*args, **kwargs)

    def save_revision(self, user=None, submitted_for_moderation=False, approved_go_live_at=None, changed=True):
        """Add applications and translation specific fields to the revision of the page."""
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
    A simple category page with a multilingual title fieldself.

    CategoryPages are simple pages that can only be created once at the root level of the CMS.
    """

    @classmethod
    def can_create_at(cls, parent):
        """Make sure the page can only be created once in the page hierarchy."""
        return super(CategoryPage, cls).can_create_at(parent) and not cls.objects.exists()

    class Meta:
        abstract = True


class HomePage(CategoryPage):
    """The root page of the LIS cms site."""

    parent_page_types = ["wagtailcore.Page"]

    class Meta:
        verbose_name = _("Homepage")
        db_table = "homepage"


class LiteraryCategoriesPage(CategoryPage):
    """A category page to place literary genres in."""

    parent_page_types = ["HomePage"]

    class Meta:
        verbose_name = _("Literary genre")
        db_table = "literary_categories"


class LiteraryCategoryPage(I18nPage):
    """A page that describes a literary category."""

    parent_page_types = ["LiteraryCategoriesPage"]

    class Meta:
        verbose_name = _("Literary genre")
        verbose_name_plural = _("Literary genres")
        db_table = "literary_category"


class ContactTypesPage(CategoryPage):
    """A category page to place types of contact in."""

    parent_page_types = ["HomePage"]

    class Meta:
        verbose_name = _("Types of contact")
        db_table = "contact_types"


class ContactTypePage(I18nPage):
    """A page that describes a type of contact."""

    parent_page_types = ["ContactTypesPage"]

    class Meta:
        verbose_name = _("Contact type")
        verbose_name_plural = _("Types of contact")
        db_table = "contact_type"


class LiteraryPeriodsPage(CategoryPage):
    """A category page to place literary periods in."""

    parent_page_types = ["HomePage"]

    class Meta:
        verbose_name = _("Literary periods")
        db_table = "literary_periods"


class LiteraryPeriodPage(I18nPage):
    """A page that describes a literary period."""

    parent_page_types = ["LiteraryPeriodsPage"]

    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("A general description of the literary period and its significance."))
    description_de = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("A general description of the literary period and its significance."))
    description_cs = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("A general description of the literary period and its significance."))
    i18n_description = TranslatedField("description", "description_de", "description_cs")

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
        ObjectList(content_panels, heading=_("Content"), classname="i18n en"),
        ObjectList(content_panels_de, heading=_("German content"), classname="i18n de"),
        ObjectList(content_panels_cs, heading=_("Czech content"), classname="i18n cz"),
        ObjectList(I18nPage.meta_panels, heading=_("Meta information")),
    ])


class LanguagesPage(CategoryPage):
    """A category page to place languages pages in spoken by the authors."""

    parent_page_types = ["HomePage"]

    class Meta:
        verbose_name = _("Languages")
        db_table = "languages"


class LanguagePage(I18nPage):
    """A page that describes a contact type."""

    parent_page_types = ["LanguagesPage"]

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")
        db_table = "language"


class AuthorsPage(CategoryPage):
    """A category page to place author pages in."""

    parent_page_types = ["HomePage"]

    class Meta:
        verbose_name = _("Authors")
        db_table = "authors"


class AuthorPage(I18nPage):
    """A page that describes an author."""

    parent_page_types = ["AuthorsPage"]

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
        related_name='+',
        verbose_name=_("Title image"),
        help_text=_("A meaningful image that will be used to present the author to the user."))
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        default=SEX_UNKNOWN,
        verbose_name=_("Sex"))
    date_of_birth_year = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        verbose_name=_("Year of birth"),
        help_text=_("The year that the author is born in."))
    date_of_birth_month = models.PositiveSmallIntegerField(
        choices=dates.MONTHS.items(),
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name=_("Month of birth"),
        help_text=_("The month that the author is born in."))
    date_of_birth_day = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        verbose_name=_("Day of birth"),
        help_text=_("The day that the author is born on."))
    date_of_death_year = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        verbose_name=_("Year of death"),
        help_text=_("The year that the author died in."))
    date_of_death_month = models.PositiveSmallIntegerField(
        choices=dates.MONTHS.items(),
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name=_("Month of death"),
        help_text=_("The month that the author died in."))
    date_of_death_day = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        verbose_name=_("Day of death"),
        help_text=_("The day that the author died at."))

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
            "languages",
            label=_("Languages"),
            min_num=0,
            help_text=_("The languages that the author has been active in."),
            panels=[PageChooserPanel("language", "cms.LanguagePage")]
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
            label=_("Literary genres"),
            min_num=0,
            help_text=_("The literary genres the author is associated with."),
            panels=[PageChooserPanel("literary_category", "cms.LiteraryCategoryPage")]
        )
    ]

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
        ObjectList(I18nPage.meta_panels, heading=_("Meta information"))])

    def __init__(self, *args, **kwargs):
        self._meta.get_field("slug").default = BLANK_TEXT
        super(AuthorPage, self).__init__(*args, **kwargs)

    def clean(self):
        """Add autogenerated values for non-editable required fields."""
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
        """Add more context information on view requests."""
        context = super(AuthorPage, self).get_context(request, *args, **kwargs)
        context["sub_pages"] = self.get_children().specific()
        # context["memorial_sites"] = self.memorial_sites.all().specific()
        return context

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")


class AuthorPageName(Orderable):
    """A join relation that holds the name of an author."""

    author = ParentalKey("AuthorPage", related_name="names")

    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Title"),
        help_text=_("Academic title of the author if any."))
    title_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Title"),
        help_text=_("Academic title of the author in German."))
    title_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Title"),
        help_text=_("Academic title of the author in Czech."))
    i18n_title = TranslatedField("title", "title_de", "title_cs")

    first_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("First name"))
    first_name_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("First name"),
        help_text=_("The first name in German if different from international spelling."))
    first_name_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("First name"),
        help_text=_("The first name in Czech if different from international spelling."))
    i18n_first_name = TranslatedField("first_name", "first_name_de", "first_name_cs")

    last_name = models.CharField(
        max_length=255,
        verbose_name=_("Last name"))
    last_name_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Last name"),
        help_text=_("The last name in German if different from international spelling."))
    last_name_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Last name"),
        help_text=_("The first name in Czech if different from international spelling."))
    i18n_last_name = TranslatedField("last_name", "last_name_de", "last_name_cs")

    birth_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Birth name"),
        help_text=_("Birth name of the author if different from last name."))
    birth_name_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Birth name"),
        help_text=_("Birth name of the author if different from international spelling."))
    birth_name_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Birth name"),
        help_text=_("Birth name of the author if different from international spelling."))
    i18n_birth_name = TranslatedField("birth_name", "birth_name_de", "birth_name_cs")

    is_pseudonym = models.BooleanField(
        default=False,
        verbose_name=_("Is pseudonym"),
        help_text=_("This name has been used as a pseudonym by the author."))

    def clean(self):
        """Check wether any valid name has been set."""
        super(AuthorPageName, self).clean()
        if not self.first_name and not self.last_name:
            raise ValidationError(_("Name entries must at least contain a first name or a last name."))

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
    """A join instance that creates a relation between an author and a literary period he has been involved in."""

    author = ParentalKey(
        AuthorPage,
        related_name="literary_periods",
        verbose_name=_("Author"),
        help_text=_("Author that this mapping is referencing."))
    literary_period = models.ForeignKey(
        LiteraryPeriodPage,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="authors",
        verbose_name=_("Literary period"),
        help_text=_("Literary period that the author is associated with."))

    def __str__(self):
        return str(self.literary_period)

    class Meta:
        db_table = "author_literary_period"


class AuthorLiteraryCategory(Orderable):
    """Join relation that creates a connection between an author and the literary genre he has been involved in."""

    author = ParentalKey("AuthorPage", related_name="literary_categories")
    literary_category = models.ForeignKey(
        LiteraryCategoryPage,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="authors",
        verbose_name=_("Literary genre"),
        help_text=_("Literary genre that the author is associated with."))

    def __str__(self):
        return str(self.literary_category)

    class Meta:
        db_table = "author_literary_category"


class AuthorLanguage(Orderable):
    """Join relation that creates a connection between an author and the languages he is associated with."""

    author = ParentalKey("AuthorPage", related_name="languages")
    language = models.ForeignKey(
        "LanguagePage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="authors",
        verbose_name=_("Language"),
        help_text=_("Language that the author has been active in."))

    def __str__(self):
        return str(self.language)

        class Meta:
            db_table = "author_language"


class LevelPage(I18nPage):
    """A simple mixin that adds methods to list the models text types as an iterable."""

    parent_page_types = ["AuthorPage"]

    TEXT_TYPES = ()

    @classmethod
    def can_create_at(cls, parent):
        """Determine the valid location of the page in the page hierarchy."""
        return super(LevelPage, cls).can_create_at(parent) and not parent.get_children().exact_type(cls)

    def get_url_parts(self, *args, **kwargs):
        return self.get_parent().get_url_parts(*args, **kwargs)

    def get_texts(self):
        """Return the text type fields of the page as an iterable."""
        texts = []
        for text_type in self.TEXT_TYPES:
            attr = "i18n_" + text_type
            prop = getattr(self, attr, None)
            if prop:
                texts.append((_(text_type.capitalize()), prop))
        return texts

    class Meta:
        abstract = True


class Level1Page(LevelPage):
    """The 'Discover' page of the LIS domain."""

    TEXT_TYPES = ("biography", "works")

    biography = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        default=[],
        verbose_name=_("Biography"),
        help_text=_("An introductory biography of the author aimed at laymen."))
    biography_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Biography"),
        help_text=_("An introductory biography of the author aimed at laymen."))
    biography_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Biography"),
        help_text=_("An introductory biography of the author aimed at laymen."))
    i18n_biography = TranslatedField("biography", "biography_de", "biography_cs")

    works = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Literary works"),
        help_text=_("An introduction to the works of the author aimed at laymen."))
    works_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Literary works"),
        help_text=_("An introduction to the works of the author aimed at laymen."))
    works_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Literary works"),
        help_text=_("An introduction to the works of the author aimed at laymen."))
    i18n_works = TranslatedField("works", "works_de", "works_cs")

    default_panels = [
        StreamFieldPanel("biography"),
        StreamFieldPanel("works")]
    german_panels = [
        StreamFieldPanel("biography_de"),
        StreamFieldPanel("works_de")]
    czech_panels = [
        StreamFieldPanel("biography_cs"),
        StreamFieldPanel("works_cs")]
    edit_handler = TabbedInterface([
        ObjectList(default_panels, heading=_("English"), classname="i18n en"),
        ObjectList(german_panels, heading=_("German"), classname="i18n de"),
        ObjectList(czech_panels, heading=_("Czech"), classname="i18n cz"),
        ObjectList(I18nPage.meta_panels, heading=_("Meta information"))])

    def get_admin_display_title(self):
        """Return title to be displayed in the admins UI."""
        return f"I. {self.i18n_draft_title or self.i18n_title}"

    def full_clean(self, *args, **kwargs):
        """Set default title."""
        self.title = "Discovery"
        self.title_de = "Entdecken"
        self.title_cs = "Discovery*"
        super(Level1Page, self).full_clean(*args, **kwargs)

    def __str__(self):
        return f"I. {self.i18n_title}"

    class Meta:
        db_table = "level_1"
        verbose_name = _("I. Discovery")


class Level2Page(LevelPage):
    """The 'Deepen' page of the LIS domain."""

    TEXT_TYPES = ("biography", "works", "reception", "connections", "full_texts")

    biography = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Biography"),
        help_text=_("An introductory biography of the author aimed at laymen."))
    biography_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Biography"),
        help_text=_("An introductory biography of the author aimed at laymen."))
    biography_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Biography"),
        help_text=_("An introductory biography of the author aimed at laymen."))
    i18n_biography = TranslatedField("biography", "biography_de", "biography_cs")

    works = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Literary works"),
        help_text=_("An introduction to the works of the author aimed at laymen."))
    works_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Literary works"),
        help_text=_("An introduction to the works of the author aimed at laymen."))
    works_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Literary works"),
        help_text=_("An introduction to the works of the author aimed at laymen."))
    i18n_works = TranslatedField("works", "works_de", "works_cs")

    reception = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Reception"),
        help_text=_("A more in-depth description for interested users on how the author has been received."))
    reception_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Reception"),
        help_text=_("A more in-depth description for interested users on how the author has been received."))
    reception_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Reception"),
        help_text=_("A more in-depth description for interested users on how the author has been received."))
    i18n_reception = TranslatedField("reception", "reception_de", "reception_cs")

    connections = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Connections"),
        help_text=_("TODO"))
    connections_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Connections"),
        help_text=_("TODO"))
    connections_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Connections"),
        help_text=_("TODO"))
    i18n_connections = TranslatedField("connections", "connections_de", "connections_cs")

    full_texts = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Full texts"),
        help_text=_("TODO"))
    full_texts_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Full texts"),
        help_text=_("TODO"))
    full_texts_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Full texts"),
        help_text=_("TODO"))
    i18n_full_texts = TranslatedField("full_texts", "full_texts_de", "full_texts_cs")

    default_panels = [
        StreamFieldPanel("biography"),
        StreamFieldPanel("works"),
        StreamFieldPanel("reception"),
        StreamFieldPanel("connections"),
        StreamFieldPanel("full_texts")]
    german_panels = [
        StreamFieldPanel("biography_de"),
        StreamFieldPanel("works_de"),
        StreamFieldPanel("reception_de"),
        StreamFieldPanel("connections_de"),
        StreamFieldPanel("full_texts_de")]
    czech_panels = [
        StreamFieldPanel("biography_cs"),
        StreamFieldPanel("works_cs"),
        StreamFieldPanel("reception_cs"),
        StreamFieldPanel("connections_cs"),
        StreamFieldPanel("full_texts_cs")]

    edit_handler = TabbedInterface([
        ObjectList(default_panels, heading=_("English"), classname="i18n en"),
        ObjectList(german_panels, heading=_("German"), classname="i18n de"),
        ObjectList(czech_panels, heading=_("Czech"), classname="i18n cz"),
        ObjectList(I18nPage.meta_panels, heading=_("Meta information"))])

    def get_admin_display_title(self):
        """Return title to be displayed in the admins UI."""
        return f"II. {self.i18n_draft_title or self.i18n_title}"

    def full_clean(self, *args, **kwargs):
        """Set default title."""
        self.title = "Delving deeper"
        self.title_de = "Vertiefen"
        self.title_cs = "Deepen*"
        super(Level2Page, self).full_clean(*args, **kwargs)

    def __str__(self):
        return f"II. {self.i18n_title}"

    class Meta:
        db_table = "level_2"
        verbose_name = _("II. Delving deeper")


class Level3Page(LevelPage):
    """The 'Research' page of the LIS domain."""

    TEXT_TYPES = ("primary_literature", "testimony", "secondary_literature")

    primary_literature = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Primary literature"),
        help_text=_("A more in-depth presentation of primary literature of the author for an academic user."))
    primary_literature_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Primary literature"),
        help_text=_("A more in-depth presentation of primary literature of the author for an academic user."))
    primary_literature_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Primary literature"),
        help_text=_("A more in-depth presentation of primary literature of the author for an academic user."))
    i18n_primary_literature = TranslatedField("primary_literature", "primary_literature_de", "primary_literature_cs")

    testimony = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Testimony"),
        help_text=_("TODO"))
    testimony_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Testimony"),
        help_text=_("TODO"))
    testimony_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Testimony"),
        help_text=_("TODO"))
    i18n_testimony = TranslatedField("testimony", "testimony_de", "testimony_cs")

    secondary_literature = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Secondary literature"),
        help_text=_("Further secondary literature about the author and his works aimed at academic users."))
    secondary_literature_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Secondary literature"),
        help_text=_("Further secondary literature about the author and his works aimed at academic users."))
    secondary_literature_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Secondary literature"),
        help_text=_("Further secondary literature about the author and his works aimed at academic users."))
    i18n_secondary_literature = TranslatedField(
        "secondary_literature",
        "secondary_literature_de",
        "secondary_literature_cs")

    default_panels = [
        StreamFieldPanel("primary_literature"),
        StreamFieldPanel("testimony"),
        StreamFieldPanel("secondary_literature")]
    german_panels = [
        StreamFieldPanel("primary_literature_de"),
        StreamFieldPanel("testimony_de"),
        StreamFieldPanel("secondary_literature_de")]
    czech_panels = [
        StreamFieldPanel("primary_literature_cs"),
        StreamFieldPanel("testimony_cs"),
        StreamFieldPanel("secondary_literature_cs")]
    edit_handler = TabbedInterface([
        ObjectList(default_panels, heading=_("English"), classname="i18n en"),
        ObjectList(german_panels, heading=_("German"), classname="i18n de"),
        ObjectList(czech_panels, heading=_("Czech"), classname="i18n cz"),
        ObjectList(I18nPage.meta_panels, heading=_("Meta information"))])

    def get_admin_display_title(self):
        """Return title to be displayed in the admins UI."""
        return f"III. {self.i18n_draft_title or self.i18n_title}"

    def full_clean(self, *args, **kwargs):
        """Set default title."""
        self.title = "Research literature"
        self.title_de = "Forschen"
        self.title_cs = "Research literature*"
        super(Level3Page, self).full_clean(*args, **kwargs)

    def __str__(self):
        return f"III. {self.i18n_title}"

    class Meta:
        db_table = "level_3"
        verbose_name = _("III. Research literature")


class LocationTypesPage(CategoryPage):
    """A category page to place types of location in."""

    parent_page_types = ["HomePage"]

    class Meta:
        verbose_name = _("Types of locations")
        db_table = "location_types"


class LocationTypePage(I18nPage):
    """A descriptive type of a location."""

    parent_page_types = ["LocationTypesPage"]

    class Meta:
        verbose_name = _("Type of location")
        verbose_name_plural = _("Types of locations")
        db_table = "location_type"


class LocationsPage(CategoryPage):
    """A category page to place locations in."""

    parent_page_types = ["HomePage"]

    class Meta:
        verbose_name = _("Locations")
        db_table = "locations"


class LocationPage(I18nPage):
    """A geographic place on earth."""

    parent_page_types = ["LocationsPage"]

    title_image = models.ForeignKey(
        ImageMedia,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Title image"),
        help_text=_("A meaningful image that will be used to present the location to the user."))
    location_type = models.ForeignKey(
        "LocationTypePage",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="locations",
        verbose_name=_("Type of location"))

    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("A short general description of the location without any relation to specific authors."))
    description_de = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("A short general description of the location without any relation to specific authors."))
    description_cs = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("A short general description of the location without any relation to specific authors."))
    i18n_description = TranslatedField("description", "description_de", "description_cs")

    address = models.TextField(
        blank=True,
        verbose_name=_("Address"),
        help_text=_("The postal address of the location if any."))
    address_de = models.TextField(
        blank=True,
        verbose_name=_("Address"),
        help_text=_("The postal address of the location if any."))
    address_cs = models.TextField(
        blank=True,
        verbose_name=_("Address"),
        help_text=_("The postal address of the location if any."))
    i18n_address = TranslatedField("address", "address_de", "address_cs")

    directions = models.TextField(
        blank=True,
        verbose_name=_("How to get there"),
        help_text=_("A short description of directions to find the location."))
    directions_de = models.TextField(
        blank=True,
        verbose_name=_("How to get there"),
        help_text=_("A short description of directions to find the location."))
    directions_cs = models.TextField(
        blank=True,
        verbose_name=_("How to get there"),
        help_text=_("A short description of directions to find the location."))
    i18n_directions = TranslatedField("directions", "directions_de", "directions_cs")

    coordinates = PointField(
        verbose_name=_("Location coordinates"),
        help_text=_("The actual geographic location."))

    search_fields = I18nPage.search_fields + [
        index.SearchField("description"),
        index.SearchField("description_de"),
        index.SearchField("description_cs"),
        index.SearchField("directions"),
        index.SearchField("directions_de"),
        index.SearchField("directions_cs")]

    default_panels = [
        FieldPanel("title", classname="full title"),
        ImageChooserPanel("title_image"),
        PageChooserPanel("location_type", "cms.LocationTypePage"),
        InlinePanel(
            "contacts",
            label=_("Contact information"),
            min_num=0,
            help_text=_("The authors that this memorial site is dedicated to."),
            panels=[
                PageChooserPanel("contact_type", "cms.ContactTypePage"),
                FieldPanel("name"),
                FieldPanel("name_de"),
                FieldPanel("name_cs")]),
        FieldPanel("description"),
        FieldPanel("address"),
        FieldPanel("directions"),
        FieldPanel("coordinates", widget=GooglePointFieldWidget()),
    ]
    german_panels = [
        FieldPanel("title_de", classname="full title"),
        FieldPanel("description_de"),
        FieldPanel("address_de"),
        FieldPanel("directions_de")]
    czech_panels = [
        FieldPanel("title_cs", classname="full title"),
        FieldPanel("description_cs"),
        FieldPanel("address_cs"),
        FieldPanel("directions_cs")]
    edit_handler = TabbedInterface([
        ObjectList(default_panels, heading=_("English")),
        ObjectList(german_panels, heading=_("German"), classname="i18n en"),
        ObjectList(czech_panels, heading=_("Czech"), classname="i18n de"),
        ObjectList(I18nPage.meta_panels, heading=_("Meta information"))])

    def __str__(self):
        return self.i18n_title

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        db_table = "location"


class LocationPageContact(Orderable):
    """A join relation holding contact information about a location."""

    location = ParentalKey("LocationPage", related_name="contacts")
    contact_type = models.ForeignKey(
        ContactTypePage,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="contacts",
        verbose_name=_("Contact type"))

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"))
    name_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("German name"))
    name_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Czech name"))
    i18n_name = TranslatedField("name", "name_de", "name_cs")


class MemorialSitePage(I18nPage):
    """A memorial reference between a geographic location and an author."""

    parent_page_types = ["LocationPage"]

    title_image = models.ForeignKey(
        ImageMedia,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Title image"),
        help_text=_("A meaningful image that will be used to present the memorial site to the user."))
    description = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Description"),
        help_text=_("A description of the memorial site and its significance to the referenced authors."))
    description_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Description"),
        help_text=_("A description of the memorial site and its significance to the referenced authors."))
    description_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Description"),
        help_text=_("A description of the memorial site and its significance to the referenced authors."))
    i18n_description = TranslatedField("description", "description_de", "description_cs")

    detailed_description = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Detailed description"),
        help_text=_("A detailed description of the memorial site and its significance to the referenced authors."))
    detailed_description_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Detailed description"),
        help_text=_("A detailed description of the memorial site and its significance to the referenced authors."))
    detailed_description_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_("Detailed description"),
        help_text=_("A detailed description of the memorial site and its significance to the referenced authors."))
    i18n_detailed_description = TranslatedField(
        "detailed_description",
        "detailed_description_de",
        "detailed_description_cs")

    default_panels = [
        ImageChooserPanel("title_image"),
        InlinePanel(
            "authors",
            label=_("Authors"),
            min_num=1,
            help_text=_("The authors that this memorial site is dedicated to."),
            panels=[PageChooserPanel("author", "cms.AuthorPage")]),
        StreamFieldPanel("description"),
        StreamFieldPanel("detailed_description")]
    german_panels = [
        StreamFieldPanel("description_de"),
        StreamFieldPanel("detailed_description_de")]
    czech_panels = [
        StreamFieldPanel("description_cs"),
        StreamFieldPanel("detailed_description_de")]
    edit_handler = TabbedInterface([
        ObjectList(default_panels, heading=_("English")),
        ObjectList(german_panels, heading=_("German")),
        ObjectList(czech_panels, heading=_("Czech")),
        ObjectList(I18nPage.meta_panels, heading=_("Meta information"))])

    def full_clean(self, *args, **kwargs):
        """Set the title of the page to the authors name that are referenced by the memorial."""
        title = ", ".join([x.author.title for x in self.authors.all()])
        self.title = title
        self.title_de = title
        self.title_cs = title
        self.slug = text.slugify(self.title)
        super(MemorialSitePage, self).full_clean(*args, **kwargs)

    def __str__(self):
        return f"{_('Memorial site')} {super(MemorialSitePage, self).__str__()}"

    class Meta:
        verbose_name = _("Memorial site")
        verbose_name_plural = _("Memorial sites")
        db_table = "memorial_site"


class MemorialSiteAuthor(Orderable):
    """Join page type to add multiple authors to one memorial site."""

    memorial_site = ParentalKey(
        "MemorialSitePage",
        related_name="authors",
        verbose_name=_("Memorial site"),
        help_text=_("The memorial site this mapping references to."))
    author = models.ForeignKey(
        AuthorPage,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="memorial_sites",
        verbose_name=_("Author"),
        help_text=_("The author that is remebered by this memorial site."))

    class Meta:
        db_table = "memorial_site_author"
