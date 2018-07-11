"""Custom page models that describe the LIS data schema."""

import logging
from collections import namedtuple
from typing import List, NewType, Tuple

from django.contrib.gis.db.models import PointField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import dates, text
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_noop, override, pgettext
from mapwidgets import GooglePointFieldWidget
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, PageChooserPanel,
                                         StreamFieldPanel, TabbedInterface)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from dal import autocomplete

from .blocks import ParagraphStructBlock
from .helpers import TranslatedField, format_date, validate_date
from . import tags
from .media import ImageMedia
from .messages import TXT

LOGGER = logging.getLogger("wagtail.core")
DB_TABLE_PREFIX = "cms_"
GENDER = NewType("Gender", str)
GENDER_OPTION = Tuple[GENDER, str]

EDITOR_FEATURES = [
    "bold",
    "italic",
    "strikethrough",
    "sup",
    "ol",
    "ul",
    "hr",
    "blockquote",
    "link",
]

TextType = namedtuple("TextType", [
    "field",
    "heading"
])


# TODO: Rename to CmsPage
class I18nPage(Page):
    """
    An abstract base page class that supports translated content.

    The class should be used for all page types of the CMS.

    Overrides Page.save and Page.save_revision methods to make sure
    multilingual content is handled the same as the default fields.

    """

    ORIGINAL_LANGUAGE_ENGLISH = "en"
    ORIGINAL_LANGUAGE_GERMAN = "de"
    ORIGINAL_LANGUAGE_CZECH = "cs"
    ORIGINAL_LANGUAGE = (
        (ORIGINAL_LANGUAGE_ENGLISH, _(TXT["language.en"])),
        (ORIGINAL_LANGUAGE_GERMAN, _(TXT["language.de"])),
        (ORIGINAL_LANGUAGE_CZECH, _(TXT["language.cs"])),
    )
    RICH_TEXT_FEATURES = ["bold", "italic", "strikethrough", "link"]

    title_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["page.title_de"]),
        help_text=_(TXT["page.title_de.help"])
    )
    title_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["page.title_cs"]),
        help_text=_(TXT["page.title_cs.help"])
    )
    i18n_title = TranslatedField.named("title", True)

    draft_title_de = models.CharField(
        max_length=255,
        blank=True,
        editable=False,
        verbose_name=_(TXT["page.draft_title_de"]),
        help_text=_(TXT["page.draft_title_de.help"])
    )
    draft_title_cs = models.CharField(
        max_length=255,
        blank=True,
        editable=False,
        verbose_name=_(TXT["page.draft_title_cs"]),
        help_text=_(TXT["page.draft_title_cs.help"])
    )
    i18n_draft_title = TranslatedField.named("draft_title", True)

    editor = models.CharField(
        max_length=2048,
        verbose_name=_(TXT["page.editor"]),
        help_text=_(TXT["page.editor.help"])
    )
    original_language = models.CharField(
        max_length=3,
        choices=ORIGINAL_LANGUAGE,
        default=ORIGINAL_LANGUAGE_GERMAN,
        verbose_name=_(TXT["page.original_language"]),
        help_text=_(TXT["page.original_language.help"])
    )

    is_creatable = False
    search_fields = Page.search_fields + [
        index.SearchField('title_de', partial_match=True, boost=2),
        index.SearchField('title_cs', partial_match=True, boost=2)
    ]
    english_panels = [
        FieldPanel("title", classname="full title"),
    ]
    german_panels = [
        FieldPanel("title_de", classname="full title"),
    ]
    czech_panels = [
        FieldPanel("title_cs", classname="full title"),
    ]
    meta_panels = [
        FieldPanel("owner"),
        FieldPanel("editor"),
        FieldPanel("original_language"),
    ]
    edit_handler = TabbedInterface([
        ObjectList(english_panels, heading=_(TXT["heading.en"])),
        ObjectList(german_panels, heading=_(TXT["heading.de"])),
        ObjectList(czech_panels, heading=_(TXT["heading.cs"])),
        ObjectList(meta_panels, heading=_(TXT["heading.meta"])),
    ])

    def get_admin_display_title(self):
        """Return title to be displayed in the admins UI."""
        return self.i18n_draft_title or self.i18n_title

    def full_clean(self, *args, **kwargs):
        """Set the translated draft titles according the translated title fields."""
        if not self.draft_title_de:
            self.draft_title_de = self.title_de
        if not self.draft_title_cs:
            self.draft_title_cs = self.title_cs
        super(I18nPage, self).full_clean(*args, **kwargs)

    def save_revision(
            self,
            user=None,
            submitted_for_moderation=False,
            approved_go_live_at=None,
            changed=True):
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
        LOGGER.info(f"Page edited: \"{self.title}\" id={self.id} revision_id={revision.id}")

        if submitted_for_moderation:
            LOGGER.info(f""""
            Page submitted for moderation: \"{self.title}\" id={self.id} revision_id={revision.id}
            """)

        return revision

    def __str__(self):
        return str(self.i18n_title)


class CategoryPage(I18nPage):
    """
    A simple category page with a multilingual title fieldself.

    CategoryPages are simple pages that can only be created once at the root level of the CMS.
    """

    # class properties
    icon_class = "fas fa-tags"
    template = "cms/categories/category_page.html"

    @classmethod
    def can_create_at(cls, parent):
        """Make sure the page can only be created once in the page hierarchy."""
        return super(CategoryPage, cls).can_create_at(parent) and not cls.objects.exists()

    def get_context(self, request, *args, **kwargs):
        """Add child pages into the pages context."""
        context = super(CategoryPage, self).get_context(request, *args, **kwargs)
        child_pages = self.get_children().specific().live()

        context["child_pages"] = sorted(child_pages, key=lambda x: str(x.i18n_title))

        return context

    class Meta:
        abstract = True


class HomePage(CategoryPage):
    """The root page of the LIS cms site."""

    icon_class = "fas fas-home"
    parent_page_types = ["wagtailcore.Page"]

    class Meta:
        db_table = "homepage"  # TODO: Add prefix
        verbose_name = _(TXT["home"])
        verbose_name_plural = _(TXT["home.plural"])


class LiteraryCategoriesPage(CategoryPage):
    """A category page to place literary genres in."""

    parent_page_types = ["HomePage"]
    template = CategoryPage.template

    class Meta:
        db_table = "literary_categories"  # TODO: Add prefix
        verbose_name = _(TXT["genre.plural"])


class LiteraryCategoryPage(I18nPage):
    """A page that describes a literary category."""

    icon_class = "fas fa-tag"
    parent_page_types = ["LiteraryCategoriesPage"]

    class Meta:
        db_table = "literary_category"  # TODO: Add prefix
        verbose_name = _(TXT["genre"])
        verbose_name_plural = _(TXT["genre.plural"])


class ContactTypesPage(CategoryPage):
    """A category page to place types of contact in."""

    parent_page_types = ["HomePage"]
    template = CategoryPage.template

    class Meta:
        db_table = "contact_types"  # TODO: Add prefix
        verbose_name = _(TXT["contact_type.plural"])


class ContactTypePage(I18nPage):
    """A page that describes a type of contact."""

    icon_class = "fas fa-tag"
    parent_page_types = ["ContactTypesPage"]

    class Meta:
        db_table = "contact_type"  # TODO: Add prefix
        verbose_name = _(TXT["contact_type"])
        verbose_name_plural = _(TXT["contact_type.plural"])


class LiteraryPeriodsPage(CategoryPage):
    """A category page to place literary periods in."""

    parent_page_types = ["HomePage"]
    template = CategoryPage.template

    class Meta:
        db_table = "literary_periods"  # TODO: Add prefix
        verbose_name = _(TXT["literary_period.plural"])


class LiteraryPeriodPage(I18nPage):
    """A page that describes a literary period."""

    icon_class = "fas fa-tag"
    parent_page_types = ["LiteraryPeriodsPage"]

    description = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["literary_period.description"]),
        help_text=_(TXT["literary_period.description.help"])
    )
    description_de = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["literary_period.description"]),
        help_text=_(TXT["literary_period.description.help"])
    )
    description_cs = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["literary_period.description"]),
        help_text=_(TXT["literary_period.description.help"])
    )
    i18n_description = TranslatedField.named("description")

    english_panels = I18nPage.english_panels + [
        FieldPanel("description"),
    ]
    german_panels = I18nPage.german_panels + [
        FieldPanel("description_de"),
    ]
    czech_panels = I18nPage.czech_panels + [
        FieldPanel("description_cs"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(english_panels, heading=_(TXT["heading.en"])),
        ObjectList(german_panels, heading=_(TXT["heading.de"])),
        ObjectList(czech_panels, heading=_(TXT["heading.cs"])),
        ObjectList(I18nPage.meta_panels, heading=_(TXT["heading.meta"])),
    ])

    class Meta:
        # TODO: Add db_table
        verbose_name = _(TXT["literary_period"])


class LanguagesPage(CategoryPage):
    """A category page to place languages pages in spoken by the authors."""

    parent_page_types = ["HomePage"]
    template = CategoryPage.template

    class Meta:
        db_table = "languages"  # TODO: Add prefix
        verbose_name = _(TXT["language.plural"])


class LanguagePage(I18nPage):
    """A page that describes a contact type."""

    icon_class = "fas fa-tag"
    parent_page_types = ["LanguagesPage"]

    class Meta:
        db_table = "language"  # TODO: Add prefix
        verbose_name = _(TXT["language"])
        verbose_name_plural = _(TXT["language.plural"])


class AuthorsPage(CategoryPage):
    """A category page to place author pages in."""

    parent_page_types = ["HomePage"]
    template = "cms/categories/authors_page.html"

    def get_context(self, request, *args, **kwargs):
        """Add more context information on view requests."""
        context = super(AuthorsPage, self).get_context(request, *args, **kwargs)

        authors = AuthorPage.objects.order_by("title")
        if request.is_preview:
            authors = (x.get_latest_revision_as_page() for x in authors)
        else:
            authors = authors.live()
        context["authors"] = authors

        return context

    class Meta:
        db_table = "authors"  # TODO: Add prefix
        verbose_name = _(TXT["author.plural"])


class AuthorPage(I18nPage):
    """A page that describes an author."""

    GENDER_UNKNOWN: GENDER = "U"
    GENDER_MALE: GENDER = "M"
    GENDER_FEMALE: GENDER = "F"
    GENDER_CHOICES: List[GENDER_OPTION] = (
        (GENDER_UNKNOWN, _(TXT["gender.unknown"])),
        (GENDER_MALE, _(TXT["gender.male"])),
        (GENDER_FEMALE, _(TXT["gender.female"])),
    )

    title_image = models.ForeignKey(
        ImageMedia,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_(TXT["author.title_image"]),
        help_text=_(TXT["author.title_image.help"])
    )
    sex = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=GENDER_UNKNOWN,
        verbose_name=_(TXT["author.gender"])
    )  # TODO: rename to gender
    date_of_birth_year = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        verbose_name=_(TXT["author.date_of_birth_year"]),
        help_text=_(TXT["author.date_of_birth_year.help"])
    )
    date_of_birth_month = models.PositiveSmallIntegerField(
        choices=dates.MONTHS.items(),
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name=_(TXT["author.date_of_birth_month"]),
        help_text=_(TXT["author.date_of_birth_month.help"])
    )
    date_of_birth_day = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        verbose_name=_(TXT["author.date_of_birth_day"]),
        help_text=_(TXT["author.date_of_birth_day.help"])
    )
    place_of_birth = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.place_of_birth"]),
        help_text=_(TXT["author.place_of_birth.help"])
    )
    place_of_birth_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.place_of_birth"]),
        help_text=_(TXT["author.place_of_birth_de.help"])
    )
    place_of_birth_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.place_of_birth"]),
        help_text=_(TXT["author.place_of_birth_cs.help"])
    )
    i18n_place_of_birth = TranslatedField.named("place_of_birth", True)

    date_of_death_year = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        verbose_name=_(TXT["author.date_of_death_year"]),
        help_text=_(TXT["author.date_of_death_year.help"])
    )
    date_of_death_month = models.PositiveSmallIntegerField(
        choices=dates.MONTHS.items(),
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name=_(TXT["author.date_of_death_month"]),
        help_text=_(TXT["author.date_of_death_month.help"])
    )
    date_of_death_day = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        verbose_name=_(TXT["author.date_of_death_day"]),
        help_text=_(TXT["author.date_of_death_day.help"])
    )
    place_of_death = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.place_of_death"]),
        help_text=_(TXT["author.place_of_death.help"])
    )
    place_of_death_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.place_of_death"]),
        help_text=_(TXT["author.place_of_death_de.help"])
    )
    place_of_death_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.place_of_death"]),
        help_text=_(TXT["author.place_of_death_cs.help"])
    )
    i18n_place_of_death = TranslatedField.named("place_of_death", True)

    language_tags = ParentalManyToManyField(
        tags.LanguageTag,
        db_table=DB_TABLE_PREFIX + "author_tag_language",
        related_name="authors",
        blank=True,
        verbose_name=_(TXT["author.language.plural"]),
        help_text=_(TXT["author.language.help"])
    )
    genre_tags = ParentalManyToManyField(
        tags.GenreTag,
        db_table=DB_TABLE_PREFIX + "author_tag_genre",
        related_name="authors",
        blank=True,
        verbose_name=_(TXT["author.genre.plural"]),
        help_text=_(TXT["author.genre.help"])
    )
    literary_period_tags = ParentalManyToManyField(
        tags.LiteraryPeriodTag,
        db_table=DB_TABLE_PREFIX + "author_tag_literary_period",
        related_name="authors",
        blank=True,
        verbose_name=_(TXT["author.literary_period.plural"]),
        help_text=_(TXT["author.literary_period.help"])
    )

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
    general_panels = [
        ImageChooserPanel("title_image"),
        InlinePanel(
            "names",
            panels=[
                FieldPanel("is_pseudonym"),
                MultiFieldPanel(
                    children=[
                        FieldPanel("title"),
                        FieldPanel("first_name"),
                        FieldPanel("last_name"),
                        FieldPanel("birth_name"),
                    ],
                    heading=_(TXT["heading.en"]),
                    classname="collapsible"
                ),
                MultiFieldPanel(
                    children=[
                        FieldPanel("title_de"),
                        FieldPanel("first_name_de"),
                        FieldPanel("last_name_de"),
                        FieldPanel("birth_name_de"),
                    ],
                    heading=_(TXT["heading.de"])
                ),
                MultiFieldPanel(
                    children=[
                        FieldPanel("title_cs"),
                        FieldPanel("first_name_cs"),
                        FieldPanel("last_name_cs"),
                        FieldPanel("birth_name_cs"),
                    ],
                    heading=_(TXT["heading.cs"])
                ),
            ],
            label=_(TXT["author.name.plural"]),
            min_num=1,
            help_text=_(TXT["author.name.help"])
        ),
        FieldPanel("sex"),
        MultiFieldPanel(
            children=[
                FieldPanel("date_of_birth_day"),
                FieldPanel("date_of_birth_month"),
                FieldPanel("date_of_birth_year")
            ],
            classname="collapsible collapsed",
            heading=_(TXT["author.date_of_birth"])
        ),
        MultiFieldPanel(
            children=[
                FieldPanel("place_of_birth"),
                FieldPanel("place_of_birth_de"),
                FieldPanel("place_of_birth_cs")
            ],
            classname="collapsible collapsed",
            heading=_(TXT["author.place_of_birth"])
        ),
        MultiFieldPanel(
            children=[
                FieldPanel("date_of_death_day"),
                FieldPanel("date_of_death_month"),
                FieldPanel("date_of_death_year")
            ],
            classname="collapsible collapsed",
            heading=_(TXT["author.date_of_death"])
        ),
        MultiFieldPanel(
            children=[
                FieldPanel("place_of_death"),
                FieldPanel("place_of_death_de"),
                FieldPanel("place_of_death_cs")
            ],
            classname="collapsible collapsed",
            heading=_(TXT["author.place_of_death"])
        ),
        InlinePanel(
            "languages",
            label=_(TXT["author.language.plural"]),
            min_num=0,
            help_text=_(TXT["author.language.help"]),
            panels=[PageChooserPanel("language", "cms.LanguagePage")]
        ),
        InlinePanel(
            "literary_categories",
            label=_(TXT["author.literary_category.plural"]),
            min_num=0,
            help_text=_(TXT["author.literary_category.help"]),
            panels=[PageChooserPanel("literary_category", "cms.LiteraryCategoryPage")]
        ),
        InlinePanel(
            "literary_periods",
            label=_(TXT["author.literary_period.plural"]),
            min_num=0,
            help_text=_(TXT["author.literary_period.help"]),
            panels=[PageChooserPanel("literary_period", "cms.LiteraryPeriodPage")]
        ),
        MultiFieldPanel(
            heading=_(TXT["tag.plural"]),
            children=[
                FieldPanel(
                    field_name="language_tags",
                    widget=autocomplete.ModelSelect2Multiple(
                        url="autocomplete-language"
                    )
                ),
                FieldPanel(
                    field_name="genre_tags",
                    widget=autocomplete.ModelSelect2Multiple(url="autocomplete-genre"),
                ),
                FieldPanel(
                    field_name="literary_period_tags",
                    widget=autocomplete.ModelSelect2Multiple(url="autocomplete-literary-period"),
                ),
            ],
        ),
    ]

    edit_handler = TabbedInterface([
        ObjectList(general_panels, heading=_(TXT["heading.general"])),
        ObjectList(I18nPage.meta_panels, heading=_(TXT["heading.meta"]))
    ])

    @property
    def full_name_title(self):
        """Return the full name of the author including her birth name to be used in titles."""
        return self.names.first().full_name_title(self.sex)

    @property
    def formatted_date_of_birth(self):
        """Format date of birth in human readable string."""
        return format_date(
            self.date_of_birth_year,
            self.date_of_birth_month,
            self.date_of_birth_day
        )

    @property
    def formatted_date_of_death(self):
        """Format date of death in human readable string."""
        return format_date(
            self.date_of_death_year,
            self.date_of_death_month,
            self.date_of_death_day
        )

    def get_languages(self, is_preview: bool = False):
        """Return a list of language pages that are linked with this author."""
        languages = []
        if is_preview:
            for through_entity in self.languages.all():
                languages.append(through_entity.language.get_latest_revision_as_page())
        else:
            for through_entity in self.languages.all():
                if through_entity.language.live:
                    languages.append(through_entity.language)
        return languages

    def get_literary_categories(self, is_preview: bool = False):
        """Return a list of genres that are linked with this author."""
        literary_categories = []
        if is_preview:
            for through_entity in self.literary_categories.all():
                literary_categories.append(
                    through_entity.literary_category.get_latest_revision_as_page())
        else:
            for through_entity in self.literary_categories.all():
                if through_entity.literary_category.live:
                    literary_categories.append(through_entity.literary_category)
        return literary_categories

    def get_literary_periods(self, is_preview: bool = False):
        """Return a list of literary periods that are linked with this author."""
        literary_periods = []
        if is_preview:
            for through_entity in self.literary_periods.all():
                literary_periods.append(
                    through_entity.literary_period.get_latest_revision_as_page())
        else:
            for through_entity in self.literary_periods.all():
                if through_entity.literary_period.live:
                    literary_periods.append(through_entity.literary_period)
        return literary_periods

    def full_clean(self, *args, **kwargs):
        """Add autogenerated values for non-editable required fields."""
        name = self.names.first()
        if name:
            self.title = name.full_name()
            self.title_de = name.full_name_de()
            self.title_cs = name.full_name_cs()
            base_slug = text.slugify(name.last_name, allow_unicode=True)
            self.slug = self._get_autogenerated_slug(base_slug)

        super(AuthorPage, self).full_clean(*args, **kwargs)

    def clean(self):
        """Validate date components of input."""
        super(AuthorPage, self).clean()
        validate_date(self.date_of_birth_year, self.date_of_birth_month, self.date_of_birth_day)
        validate_date(self.date_of_death_year, self.date_of_death_month, self.date_of_death_day)

    def get_context(self, request, *args, **kwargs):
        """Add more context information on view requests."""
        context = super(AuthorPage, self).get_context(request, *args, **kwargs)
        author = self.get_latest_revision_as_page() if request.is_preview else self
        context["author"] = author

        # add all names of author to context
        context["author_name"], *context["author_alt_names"] = author.names.order_by("sort_order")
        context["languages"] = self.get_languages(request.is_preview)
        context["literary_categories"] = self.get_literary_categories(request.is_preview)
        context["literary_periods"] = self.get_literary_periods(request.is_preview)

        # add level pages
        levels = self.get_children().specific()
        if request.is_preview:
            levels = [x.get_latest_revision_as_page() for x in levels]
        else:
            levels = levels.live()
        context["levels"] = sorted(levels, key=lambda x: x.level_order)

        # add memorial sites
        memorial_sites = MemorialSitePage.objects.filter(authors__author=self)
        if request.is_preview:
            memorial_sites = [x.get_latest_revision_as_page() for x in memorial_sites]
        else:
            memorial_sites = memorial_sites.live()
        context["memorial_sites"] = memorial_sites

        return context

    class Meta:
        # TODO: add db_table
        verbose_name = _(TXT["author"])
        verbose_name_plural = _(TXT["author.plural"])


class AuthorPageName(Orderable):
    """A join relation that holds the name of an author."""

    author = ParentalKey("AuthorPage", related_name="names")

    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.title"]),
        help_text=_(TXT["author.name.title.help"])
    )
    title_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.title"]),
        help_text=_(TXT["author.name.title_de.help"])
    )
    title_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.title"]),
        help_text=_(TXT["author.name.title_cs.help"])
    )
    i18n_title = TranslatedField.named("title", True)

    first_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.first_name"])
    )
    first_name_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.first_name"]),
        help_text=_(TXT["author.name.first_name_de.help"])
    )
    first_name_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.first_name"]),
        help_text=_(TXT["author.name.first_name_cs.help"])
    )
    i18n_first_name = TranslatedField.named("first_name", True)

    last_name = models.CharField(
        max_length=255,
        verbose_name=_(TXT["author.name.last_name"])
    )
    last_name_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.last_name"]),
        help_text=_(TXT["author.name.last_name_de.help"])
    )
    last_name_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.last_name"]),
        help_text=_(TXT["author.name.last_name_cs.help"])
    )
    i18n_last_name = TranslatedField.named("last_name", True)

    birth_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.birth_name"]),
        help_text=_(TXT["author.name.birth_name.help"])
    )
    birth_name_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.birth_name"]),
        help_text=_(TXT["author.name.birth_name_de.help"])
    )
    birth_name_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.birth_name"]),
        help_text=_(TXT["author.name.birth_name_cs.help"])
    )
    i18n_birth_name = TranslatedField.named("birth_name", True)

    is_pseudonym = models.BooleanField(
        default=False,
        verbose_name=_(TXT["author.name.is_pseudonym"]),
        help_text=_(TXT["author.name.is_pseudonym.help"])
    )

    def full_name_title(self, gender=AuthorPage.GENDER_MALE):
        """Return the full name of this name object formatted to include the birth name."""
        name = str(self)
        birth_name = self.i18n_birth_name
        if birth_name:
            if gender == AuthorPage.GENDER_FEMALE:
                addendum = pgettext("female", f"born {birth_name}")
            else:
                addendum = pgettext("male", f"born {birth_name}")
            name += f" ({addendum})"
        return name

    def clean(self):
        """Check wether any valid name has been set."""
        super(AuthorPageName, self).clean()
        if not self.first_name and not self.last_name:
            message = _(TXT["author.name.validation"])
            raise ValidationError(message)

    def full_name(self):
        """Return the full name of the author in english language."""
        return " ".join(x.strip() for x in [self.title, self.first_name, self.last_name] if x)

    def full_name_de(self):
        """Return the full name of the author in german language."""
        title = self.title_de or self.title
        first_name = self.first_name_de or self.first_name
        last_name = self.last_name_de or self.last_name
        return " ".join(x.strip() for x in [title, first_name, last_name] if x)

    def full_name_cs(self):
        """Return the full name of the author in czech language."""
        title = self.title_cs or self.title
        first_name = self.first_name_cs or self.first_name
        last_name = self.last_name_cs or self.last_name
        return " ".join(x.strip() for x in [title, first_name, last_name] if x)

    def __str__(self):
        """Return the full name of the author in the current session language."""
        components = (self.i18n_title, self.i18n_first_name, self.i18n_last_name)
        return " ".join(x.strip() for x in components if x)


class AuthorLiteraryPeriod(Orderable):
    """A through model between the relation author and literary period."""

    author = ParentalKey(
        AuthorPage,
        related_name="literary_periods",
        verbose_name=_(TXT["author_period.author"]),
        help_text=_(TXT["author_period.author.help"])
    )
    literary_period = models.ForeignKey(
        LiteraryPeriodPage,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="authors",
        verbose_name=_(TXT["author_period.period"]),
        help_text=_(TXT["author_period.period.help"])
    )

    def __str__(self):
        return str(self.literary_period)

    class Meta:
        db_table = "author_literary_period"  # TODO: Add prefix
        verbose_name = _(TXT["author_period"])
        verbose_name_plural = _(TXT["author_period.plural"])


class AuthorLiteraryCategory(Orderable):
    """A through model between the relation author and genre."""

    author = ParentalKey(
        AuthorPage,
        related_name="literary_categories",
        verbose_name=_(TXT["author_genre.author"]),
        help_text=_(TXT["author_genre.author.help"])
    )
    literary_category = models.ForeignKey(
        LiteraryCategoryPage,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="authors",
        verbose_name=_(TXT["author_genre.genre"]),
        help_text=_(TXT["author_genre.genre.help"])
    )

    def __str__(self):
        return str(self.literary_category)

    class Meta:
        db_table = "author_literary_category"  # TODO: Add prefix
        verbose_name = _(TXT["author_genre"])
        verbose_name_plural = _(TXT["author_genre.plural"])


class AuthorLanguage(Orderable):
    """A through model between the relation author and language."""

    author = ParentalKey(
        AuthorPage,
        related_name="languages",
        verbose_name=_(TXT["author_language.author"]),
        help_text=_(TXT["author_language.author.help"])
    )
    language = models.ForeignKey(
        "LanguagePage",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="authors",
        verbose_name=_(TXT["author_language.language"]),
        help_text=_(TXT["author_language.language.help"])
    )

    def __str__(self):
        return str(self.language)

    class Meta:
        db_table = "author_language"  # TODO: Add prefix
        verbose_name = _(TXT["author_language"])
        verbose_name_plural = _(TXT["author_language.plural"])


class LevelPage(I18nPage):
    """A simple mixin that adds methods to list the models text types as an iterable."""

    PAGE_TITLE = "Level page"

    parent_page_types = ["AuthorPage"]
    text_types = ()
    level_order = 0

    @classmethod
    def can_create_at(cls, parent):
        """Determine the valid location of the page in the page hierarchy."""
        return (
            super(LevelPage, cls).can_create_at(parent)
            and not parent.get_children().exact_type(cls)
        )

    def serve(self, request, *args, **kwargs):
        """Defer to the parent pages serve method."""
        return self.get_parent().specific.serve(request, *args, **kwargs)

    def get_texts(self):
        """Return the text type fields of the page as an iterable."""
        texts = []
        for text_type in self.text_types:
            prop = getattr(self, text_type.field, None)
            if prop:
                texts.append((text_type.heading, prop))
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
        help_text=_(TXT["level1.biography.help"])
    )
    biography_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level1.biography"]),
        help_text=_(TXT["level1.biography.help"])
    )
    biography_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level1.biography"]),
        help_text=_(TXT["level1.biography.help"])
    )
    i18n_biography = TranslatedField.named("biography")

    works = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level1.works"]),
        help_text=_(TXT["level1.works.help"])
    )
    works_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level1.works"]),
        help_text=_(TXT["level1.works.help"])
    )
    works_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level1.works"]),
        help_text=_(TXT["level1.works.help"])
    )
    i18n_works = TranslatedField.named("works")

    english_panels = [
        StreamFieldPanel("biography"),
        StreamFieldPanel("works")
    ]
    german_panels = [
        StreamFieldPanel("biography_de"),
        StreamFieldPanel("works_de")
    ]
    czech_panels = [
        StreamFieldPanel("biography_cs"),
        StreamFieldPanel("works_cs")
    ]
    edit_handler = TabbedInterface([
        ObjectList(english_panels, heading=_(TXT["heading.en"])),
        ObjectList(german_panels, heading=_(TXT["heading.de"])),
        ObjectList(czech_panels, heading=_(TXT["heading.cs"])),
        ObjectList(I18nPage.meta_panels, heading=_(TXT["heading.meta"])),
    ])

    class Meta:
        db_table = "level_1"  # TODO: Add prefix
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
        help_text=_(TXT["level2.biography"]))
    biography_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.biography"]),
        help_text=_(TXT["level2.biography.help"])
    )
    biography_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.biography"]),
        help_text=_(TXT["level2.biography.help"])
    )
    i18n_biography = TranslatedField.named("biography")

    works = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.works"]),
        help_text=_(TXT["level2.works.help"])
    )
    works_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.works"]),
        help_text=_(TXT["level2.works.help"])
    )
    works_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.works"]),
        help_text=_(TXT["level2.works.help"])
    )
    i18n_works = TranslatedField.named("works")

    reception = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.reception"]),
        help_text=_(TXT["level2.reception.help"])
    )
    reception_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.reception"]),
        help_text=_(TXT["level2.reception.help"])
    )
    reception_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.reception"]),
        help_text=_(TXT["level2.reception.help"])
    )
    i18n_reception = TranslatedField.named("reception")

    connections = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.connections"]),
        help_text=_(TXT["level2.connections.help"])
    )
    connections_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.connections"]),
        help_text=_(TXT["level2.connections.help"])
    )
    connections_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.connections"]),
        help_text=_(TXT["level2.connections.help"])
    )
    i18n_connections = TranslatedField.named("connections")

    full_texts = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.full_texts"]),
        help_text=_(TXT["level2.full_texts.help"])
    )
    full_texts_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.full_texts"]),
        help_text=_(TXT["level2.full_texts.help"])
    )
    full_texts_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level2.full_texts"]),
        help_text=_(TXT["level2.full_texts.help"])
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

    edit_handler = TabbedInterface([
        ObjectList(english_panels, heading=_(TXT["heading.en"])),
        ObjectList(german_panels, heading=_(TXT["heading.de"])),
        ObjectList(czech_panels, heading=_(TXT["heading.cs"])),
        ObjectList(I18nPage.meta_panels, heading=_(TXT["heading.meta"]))
    ])

    class Meta:
        db_table = "level_2"  # TODO: Add prefix
        verbose_name = _(TXT["level2"])


class Level3Page(LevelPage):
    """The 'Research' page of the LIS domain."""

    PAGE_TITLE = TXT["level3"]

    text_types = (
        TextType("i18n_primary_literature", _(TXT["level3.primary_literature"])),
        TextType("i18n_testimony", _(TXT["level3.testimony"])),
        TextType("i18n_secondary_literature", _(TXT["level3.secondary_literature"])),
    )
    level_order = 3

    primary_literature = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.primary_literature"]),
        help_text=_(TXT["level3.primary_literature.help"])
    )
    primary_literature_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.primary_literature"]),
        help_text=_(TXT["level3.primary_literature.help"])
    )
    primary_literature_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.primary_literature"]),
        help_text=_(TXT["level3.primary_literature.help"])
    )
    i18n_primary_literature = TranslatedField.named("primary_literature")

    testimony = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.testimony"]),
        help_text=_(TXT["level3.testimony.help"])
    )
    testimony_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.testimony"]),
        help_text=_(TXT["level3.testimony.help"])
    )
    testimony_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.testimony"]),
        help_text=_(TXT["level3.testimony.help"])
    )
    i18n_testimony = TranslatedField.named("testimony")

    secondary_literature = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.secondary_literature"]),
        help_text=_(TXT["level3.secondary_literature.help"])
    )
    secondary_literature_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.secondary_literature"]),
        help_text=_(TXT["level3.secondary_literature.help"])
    )
    secondary_literature_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["level3.secondary_literature"]),
        help_text=_(TXT["level3.secondary_literature.help"])
    )
    i18n_secondary_literature = TranslatedField.named("secondary_literature")

    english_panels = [
        StreamFieldPanel("primary_literature"),
        StreamFieldPanel("testimony"),
        StreamFieldPanel("secondary_literature"),
    ]
    german_panels = [
        StreamFieldPanel("primary_literature_de"),
        StreamFieldPanel("testimony_de"),
        StreamFieldPanel("secondary_literature_de"),
    ]
    czech_panels = [
        StreamFieldPanel("primary_literature_cs"),
        StreamFieldPanel("testimony_cs"),
        StreamFieldPanel("secondary_literature_cs"),
    ]
    edit_handler = TabbedInterface([
        ObjectList(english_panels, heading=_(TXT["heading.en"])),
        ObjectList(german_panels, heading=_(TXT["heading.de"])),
        ObjectList(czech_panels, heading=_(TXT["heading.cs"])),
        ObjectList(I18nPage.meta_panels, heading=_(TXT["heading.meta"]))
    ])

    class Meta:
        db_table = "level_3"  # TODO: Add prefix
        verbose_name = _(TXT["level3"])


class LocationTypesPage(CategoryPage):
    """A category page to place types of location in."""

    parent_page_types = ["HomePage"]
    template = CategoryPage.template

    class Meta:
        db_table = "location_types"  # TODO: Add prefix
        verbose_name = _(TXT["location_type.plural"])


class LocationTypePage(I18nPage):
    """A descriptive type of a location."""

    parent_page_types = ["LocationTypesPage"]

    class Meta:
        db_table = "location_type"  # TODO: Add prefix
        verbose_name = _(TXT["location_type"])
        verbose_name_plural = _(TXT["location_type.plural"])


class LocationsPage(CategoryPage):
    """A category page to place locations in."""

    icon_class = "fas fa-globe"
    parent_page_types = ["HomePage"]
    template = "cms/categories/locations_page.html"

    def get_context(self, request, *args, **kwargs):
        """Add all child geometries to context.."""
        context = super(LocationsPage, self).get_context(request, *args, **kwargs)

        locations = LocationPage.objects.all()
        if request.is_preview:
            locations = [x.get_latest_revision_as_page() for x in locations]
        else:
            locations = locations.live()
        context["locations"] = locations
        return context

    class Meta:
        db_table = "locations"  # TODO: Add prefix
        verbose_name = _(TXT["location.plural"])


class LocationPage(I18nPage):
    """A geographic place on earth."""

    icon_class = "fas fa-map-marker"
    parent_page_types = ["LocationsPage"]

    title_image = models.ForeignKey(
        ImageMedia,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_(TXT["location.title_image"]),
        help_text=_(TXT["location.title_image.help"])
    )
    location_type = models.ForeignKey(
        "LocationTypePage",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="locations",
        verbose_name=_(TXT["location_type"])
    )

    address = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["location.address"]),
        help_text=_(TXT["location.address.help"])
    )
    address_de = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["location.address"]),
        help_text=_(TXT["location.address.help"])
    )
    address_cs = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["location.address"]),
        help_text=_(TXT["location.address.help"])
    )
    i18n_address = TranslatedField.named("address", True)

    directions = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["location.directions"]),
        help_text=_(TXT["location.directions.help"])
    )
    directions_de = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["location.directions"]),
        help_text=_(TXT["location.directions.help"])
    )
    directions_cs = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["location.directions"]),
        help_text=_(TXT["location.directions.help"])
    )
    i18n_directions = TranslatedField.named("directions")

    coordinates = PointField(
        verbose_name=_(TXT["location.coordinates"]),
        help_text=_(TXT["location.coordinates.help"])
    )

    search_fields = I18nPage.search_fields + [
        index.SearchField("directions"),
        index.SearchField("directions_de"),
        index.SearchField("directions_cs"),
    ]

    general_panels = [
        ImageChooserPanel("title_image"),
        PageChooserPanel("location_type", "cms.LocationTypePage"),
        FieldPanel("coordinates", widget=GooglePointFieldWidget()),
        InlinePanel(
            "contacts",
            label=_(TXT["location.contacts"]),
            min_num=0,
            help_text=_(TXT["location.contacts.help"]),
            panels=[
                PageChooserPanel("contact_type", "cms.ContactTypePage"),
                FieldPanel("name"),
                FieldPanel("name_de"),
                FieldPanel("name_cs")
            ]
        ),
    ]
    english_panels = I18nPage.english_panels + [
        FieldPanel("address"),
        FieldPanel("directions"),
    ]
    german_panels = I18nPage.german_panels + [
        FieldPanel("address_de"),
        FieldPanel("directions_de"),
    ]
    czech_panels = I18nPage.czech_panels + [
        FieldPanel("address_cs"),
        FieldPanel("directions_cs"),
    ]
    edit_handler = TabbedInterface([
        ObjectList(general_panels, heading=_(TXT["heading.general"])),
        ObjectList(english_panels, heading=_(TXT["heading.en"])),
        ObjectList(german_panels, heading=_(TXT["heading.de"])),
        ObjectList(czech_panels, heading=_(TXT["heading.cs"])),
        ObjectList(I18nPage.meta_panels, heading=_(TXT["heading.meta"]))
    ])

    def get_context(self, request, *args, **kwargs):
        """Add child pages into the pages context."""
        context = super(LocationPage, self).get_context(request, *args, **kwargs)
        memorial_sites = self.get_children().specific()
        if not request.is_preview:
            memorial_sites = memorial_sites.live()
        else:
            memorial_sites = [x.get_latest_revision_as_page() for x in memorial_sites]
        context["memorial_sites"] = sorted(memorial_sites, key=lambda x: str(x.i18n_title))
        return context

    class Meta:
        db_table = "location"  # TODO: Add prefix
        verbose_name = _(TXT["location"])
        verbose_name_plural = _(TXT["location.plural"])


class LocationPageContact(Orderable):
    """A join relation holding contact information about a location."""

    location = ParentalKey("LocationPage", related_name="contacts")
    contact_type = models.ForeignKey(
        ContactTypePage,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="contacts",
        verbose_name=_(TXT["location_contact.contact_type"])
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_(TXT["location_contact.name"])
    )
    name_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["location_contact.name.de"])
    )
    name_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["location_contact.name.cs"])
    )
    i18n_name = TranslatedField.named("name", True)

    class Meta:
        # TODO: add db_table
        verbose_name = _(TXT["location_contact"])
        verbose_name_plural = _(TXT["location_contact.plural"])


class MemorialSitePage(I18nPage):
    """A memorial reference between a geographic location and an author."""

    icon_class = "fas fa-sign"
    parent_page_types = ["LocationPage"]

    title_image = models.ForeignKey(
        ImageMedia,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_(TXT["memorial_site.title_image"]),
        help_text=_(TXT["memorial_site.title_image.help"])
    )

    introduction = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["memorial_site.introduction"]),
        help_text=_(TXT["memorial_site.introduction.help"])
    )
    introduction_de = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["memorial_site.introduction"]),
        help_text=_(TXT["memorial_site.introduction.help"])
    )
    introduction_cs = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["memorial_site.introduction"]),
        help_text=_(TXT["memorial_site.introduction.help"])
    )
    i18n_introduction = TranslatedField.named("introduction")

    description = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["memorial_site.description"]),
        help_text=_(TXT["memorial_site.description.help"])
    )
    description_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["memorial_site.description"]),
        help_text=_(TXT["memorial_site.description.help"])
    )
    description_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["memorial_site.description"]),
        help_text=_(TXT["memorial_site.description.help"])
    )
    i18n_description = TranslatedField.named("description")

    detailed_description = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["memorial_site.detailed_description"]),
        help_text=_(TXT["memorial_site.detailed_description.help"])
    )
    detailed_description_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["memorial_site.detailed_description"]),
        help_text=_(TXT["memorial_site.detailed_description.help"])
    )
    detailed_description_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["memorial_site.detailed_description"]),
        help_text=_(TXT["memorial_site.detailed_description.help"])
    )
    i18n_detailed_description = TranslatedField.named("detailed_description")

    general_panels = [
        ImageChooserPanel("title_image"),
        InlinePanel(
            "authors",
            label=_(TXT["memorial_site.authors"]),
            min_num=1,
            help_text=_(TXT["memorial_site.authors"]),
            panels=[PageChooserPanel("author", "cms.AuthorPage")]
        ),
    ]
    english_panels = I18nPage.english_panels + [
        FieldPanel("introduction"),
        StreamFieldPanel("description"),
        StreamFieldPanel("detailed_description")
    ]
    german_panels = I18nPage.german_panels + [
        FieldPanel("introduction_de"),
        StreamFieldPanel("description_de"),
        StreamFieldPanel("detailed_description_de")
    ]
    czech_panels = I18nPage.czech_panels + [
        FieldPanel("introduction_cs"),
        StreamFieldPanel("description_cs"),
        StreamFieldPanel("detailed_description_cs")
    ]
    edit_handler = TabbedInterface([
        ObjectList(general_panels, heading=_(TXT["heading.general"])),
        ObjectList(english_panels, heading=_(TXT["heading.en"])),
        ObjectList(german_panels, heading=_(TXT["heading.de"])),
        ObjectList(czech_panels, heading=_(TXT["heading.cs"])),
        ObjectList(I18nPage.meta_panels, heading=_(TXT["heading.meta"])),
    ])

    def get_context(self, request, *args, **kwargs):
        """Add all child geometries to context.."""
        context = super(MemorialSitePage, self).get_context(request, *args, **kwargs)

        location = self.get_parent()
        if request.is_preview:
            location = location.get_latest_revision_as_page()
        context["location"] = location

        authors = [x.author for x in self.authors.all()]
        if request.is_preview:
            authors[:] = [x.get_latest_revision_as_page() for x in authors]

        context["authors"] = {}
        for author in authors:
            levels = author.get_children().specific()
            if request.is_preview:
                levels = [x.get_latest_revision_as_page() for x in levels]
            else:
                levels = levels.live()
            context["authors"][author] = sorted(levels, key=lambda x: x.level_order)

        return context

    class Meta:
        db_table = "memorial_site"  # TODO: Add prefix
        verbose_name = _(TXT["memorial_site"])
        verbose_name_plural = _(TXT["memorial_site.plural"])


class MemorialSiteAuthor(Orderable):
    """Join page type to add multiple authors to one memorial site."""

    memorial_site = ParentalKey(
        "MemorialSitePage",
        related_name="authors",
        verbose_name=_(TXT["memorial_site"]),
        help_text=_(TXT["memorial_site_author.memorial_site.help"])
    )
    author = models.ForeignKey(
        AuthorPage,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="memorial_sites",
        verbose_name=_(TXT["memorial_site_author.author"]),
        help_text=_(TXT["memorial_site_author.author.help"])
    )

    class Meta:
        db_table = "memorial_site_author"  # TODO: Add prefix
        verbose_name = _(TXT["memorial_site_author"])
        verbose_name_plural = _(TXT["memorial_site_author.plural"])
