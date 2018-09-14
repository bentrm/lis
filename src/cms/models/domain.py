"""Implements the domain specific models of the information system."""

import datetime
from typing import List

from dal import autocomplete
from django.contrib.gis.db.models import PointField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import dates, text
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.utils.translation import override, pgettext
from mapwidgets import GooglePointFieldWidget
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    PageChooserPanel,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from cms.blocks import ParagraphStructBlock
from cms.edit_handlers import FieldPanelTab, FieldPanelTabs
from cms.messages import TXT

from .base import (
    DB_TABLE_PREFIX,
    GENDER,
    GENDER_OPTION,
    CategoryPage,
    I18nPage,
    TextType,
)
from .helpers import TranslatedField, format_date, validate_date


class AuthorIndex(CategoryPage):
    """A category page to place author pages in."""

    parent_page_types = ["HomePage"]
    template = "cms/categories/author_index.html"

    def get_context(self, request, *args, **kwargs):
        """Add more context information on view requests."""
        context = super(AuthorIndex, self).get_context(request, *args, **kwargs)

        authors = Author.objects.order_by("title")
        if request.is_preview:
            authors = (x.get_latest_revision_as_page() for x in authors)
        else:
            authors = authors.live()
        context["authors"] = authors

        return context

    class Meta:
        db_table = DB_TABLE_PREFIX + "authors"
        verbose_name = _(TXT["author.plural"])


class LocationIndex(CategoryPage):
    """A category page to place locations in."""

    parent_page_types = ["HomePage"]
    template = "cms/categories/location_index.html"

    def get_context(self, request, *args, **kwargs):
        """Add all child geometries to context.."""
        context = super(LocationIndex, self).get_context(request, *args, **kwargs)

        locations = Memorial.objects.all()
        if request.is_preview:
            locations = [x.get_latest_revision_as_page() for x in locations]
        else:
            locations = locations.live()
        context["locations"] = locations
        return context

    class Meta:
        db_table = DB_TABLE_PREFIX + "locations"
        verbose_name = _(TXT["location.plural"])


class Location(I18nPage):
    """A geographic place on earth."""

    parent_page_types = []

    title_image = models.ForeignKey(
        "ImageMedia",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_(TXT["location.title_image"]),
        help_text=_(TXT["location.title_image.help"]),
    )
    location_type_tags = ParentalManyToManyField(
        "MemorialTag",
        db_table=DB_TABLE_PREFIX + "location_tag_location_type",
        related_name="locations",
        blank=False,
        verbose_name=_(TXT["location.location_type_tags.plural"]),
        help_text=_(TXT["location.location_type_tags.help"]),
    )

    address = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["location.address"]),
        help_text=_(TXT["location.address.help"]),
    )
    address_de = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["location.address"]),
        help_text=_(TXT["location.address.help"]),
    )
    address_cs = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["location.address"]),
        help_text=_(TXT["location.address.help"]),
    )
    i18n_address = TranslatedField.named("address", True)

    contact_info = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["location.contact_info"]),
        help_text=_(TXT["location.contact_info.help"]),
    )
    contact_info_de = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["location.contact_info"]),
        help_text=_(TXT["location.contact_info.help"]),
    )
    contact_info_cs = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["location.contact_info"]),
        help_text=_(TXT["location.contact_info.help"]),
    )
    i18n_contact_info = TranslatedField.named("contact_info", True)

    directions = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["location.directions"]),
        help_text=_(TXT["location.directions.help"]),
    )
    directions_de = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["location.directions"]),
        help_text=_(TXT["location.directions.help"]),
    )
    directions_cs = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["location.directions"]),
        help_text=_(TXT["location.directions.help"]),
    )
    i18n_directions = TranslatedField.named("directions")

    coordinates = PointField(
        verbose_name=_(TXT["location.coordinates"]),
        help_text=_(TXT["location.coordinates.help"]),
    )

    search_fields = I18nPage.search_fields + [
        index.SearchField("directions"),
        index.SearchField("directions_de"),
        index.SearchField("directions_cs"),
    ]

    general_panels = [
        ImageChooserPanel("title_image"),
        FieldPanel(
            "location_type_tags",
            widget=autocomplete.ModelSelect2Multiple(
                url="autocomplete-location-type",
                attrs={"data-maximum-selection-length": 1},
            ),
        ),
        FieldPanelTabs(
            children=[
                FieldPanelTab("address", heading=_(TXT["language.en"])),
                FieldPanelTab("address_de", heading=_(TXT["language.de"])),
                FieldPanelTab("address_cs", heading=_(TXT["language.cs"])),
            ],
            heading=_(TXT["location.address"]),
            show_label=False,
        ),
        FieldPanelTabs(
            children=[
                FieldPanelTab("contact_info", heading=_(TXT["language.en"])),
                FieldPanelTab("contact_info_de", heading=_(TXT["language.de"])),
                FieldPanelTab("contact_info_cs", heading=_(TXT["language.cs"])),
            ],
            heading=_(TXT["location.contact_info"]),
            show_label=False,
        ),
        FieldPanelTabs(
            children=[
                FieldPanelTab("directions", heading=_(TXT["language.en"])),
                FieldPanelTab("directions_de", heading=_(TXT["language.de"])),
                FieldPanelTab("directions_cs", heading=_(TXT["language.cs"])),
            ],
            heading=_(TXT["location.directions"]),
            show_label=False,
        ),
        FieldPanel("coordinates", widget=GooglePointFieldWidget()),
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(general_panels, heading=_(TXT["heading.general"])),
            ObjectList(I18nPage.meta_panels, heading=_(TXT["heading.meta"])),
        ]
    )

    def get_context(self, request, *args, **kwargs):
        """Add child pages into the pages context."""
        context = super(Location, self).get_context(request, *args, **kwargs)
        memorial_sites = self.get_children().specific()
        if not request.is_preview:
            memorial_sites = memorial_sites.live()
        else:
            memorial_sites = [x.get_latest_revision_as_page() for x in memorial_sites]
        context["memorial_sites"] = sorted(
            memorial_sites, key=lambda x: str(x.i18n_title)
        )
        return context

    class Meta:
        db_table = DB_TABLE_PREFIX + "archive_location"
        verbose_name = _(TXT["location"])
        verbose_name_plural = _(TXT["location.plural"])


class MemorialSite(I18nPage):
    """A memorial reference between a geographic location and an author."""

    parent_page_types = ["Location"]

    title_image = models.ForeignKey(
        "ImageMedia",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_(TXT["memorial_site.title_image"]),
        help_text=_(TXT["memorial_site.title_image.help"]),
    )

    introduction = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["memorial_site.introduction"]),
        help_text=_(TXT["memorial_site.introduction.help"]),
    )
    introduction_de = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["memorial_site.introduction"]),
        help_text=_(TXT["memorial_site.introduction.help"]),
    )
    introduction_cs = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["memorial_site.introduction"]),
        help_text=_(TXT["memorial_site.introduction.help"]),
    )
    i18n_introduction = TranslatedField.named("introduction")

    description = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["memorial_site.description"]),
        help_text=_(TXT["memorial_site.description.help"]),
    )
    description_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["memorial_site.description"]),
        help_text=_(TXT["memorial_site.description.help"]),
    )
    description_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["memorial_site.description"]),
        help_text=_(TXT["memorial_site.description.help"]),
    )
    i18n_description = TranslatedField.named("description")

    detailed_description = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["memorial_site.detailed_description"]),
        help_text=_(TXT["memorial_site.detailed_description.help"]),
    )
    detailed_description_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["memorial_site.detailed_description"]),
        help_text=_(TXT["memorial_site.detailed_description.help"]),
    )
    detailed_description_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["memorial_site.detailed_description"]),
        help_text=_(TXT["memorial_site.detailed_description.help"]),
    )
    i18n_detailed_description = TranslatedField.named("detailed_description")

    general_panels = [
        ImageChooserPanel("title_image"),
        InlinePanel(
            "authors",
            label=_(TXT["memorial_site.authors"]),
            min_num=1,
            help_text=_(TXT["memorial_site.authors"]),
            panels=[PageChooserPanel("author", "cms.Author")],
        ),
    ]
    english_panels = I18nPage.english_panels + [
        FieldPanel("introduction"),
        StreamFieldPanel("description"),
        StreamFieldPanel("detailed_description"),
    ]
    german_panels = I18nPage.german_panels + [
        FieldPanel("introduction_de"),
        StreamFieldPanel("description_de"),
        StreamFieldPanel("detailed_description_de"),
    ]
    czech_panels = I18nPage.czech_panels + [
        FieldPanel("introduction_cs"),
        StreamFieldPanel("description_cs"),
        StreamFieldPanel("detailed_description_cs"),
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(general_panels, heading=_(TXT["heading.general"])),
            ObjectList(english_panels, heading=_(TXT["heading.en"])),
            ObjectList(german_panels, heading=_(TXT["heading.de"])),
            ObjectList(czech_panels, heading=_(TXT["heading.cs"])),
            ObjectList(I18nPage.meta_panels, heading=_(TXT["heading.meta"])),
        ]
    )

    def get_context(self, request, *args, **kwargs):
        """Add all child geometries to context.."""
        context = super(MemorialSite, self).get_context(request, *args, **kwargs)

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
        db_table = DB_TABLE_PREFIX + "archive_memorial_site"
        verbose_name = _(TXT["memorial_site"])
        verbose_name_plural = _(TXT["memorial_site.plural"])


class MemorialSiteAuthor(Orderable):
    """Join page type to add multiple authors to one memorial site."""

    memorial_site = ParentalKey(
        "MemorialSite",
        related_name="authors",
        verbose_name=_(TXT["memorial_site"]),
        help_text=_(TXT["memorial_site_author.memorial_site.help"]),
    )
    author = models.ForeignKey(
        "Author",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="memorial_sites",
        verbose_name=_(TXT["memorial_site_author.author"]),
        help_text=_(TXT["memorial_site_author.author.help"]),
    )

    class Meta:
        db_table = DB_TABLE_PREFIX + "archive_memorial_site_author"
        verbose_name = _(TXT["memorial_site_author"])
        verbose_name_plural = _(TXT["memorial_site_author.plural"])


class Author(I18nPage):
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
        "ImageMedia",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_(TXT["author.title_image"]),
        help_text=_(TXT["author.title_image.help"]),
    )
    sex = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=GENDER_UNKNOWN,
        verbose_name=_(TXT["author.gender"]),
    )  # TODO: rename to gender
    date_of_birth_year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        verbose_name=_(TXT["author.date_of_birth_year"]),
        help_text=_(TXT["author.date_of_birth_year.help"]),
    )
    date_of_birth_month = models.PositiveSmallIntegerField(
        choices=dates.MONTHS.items(),
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name=_(TXT["author.date_of_birth_month"]),
        help_text=_(TXT["author.date_of_birth_month.help"]),
    )
    date_of_birth_day = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        verbose_name=_(TXT["author.date_of_birth_day"]),
        help_text=_(TXT["author.date_of_birth_day.help"]),
    )
    place_of_birth = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.place_of_birth"]),
        help_text=_(TXT["author.place_of_birth.help"]),
    )
    place_of_birth_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.place_of_birth"]),
        help_text=_(TXT["author.place_of_birth_de.help"]),
    )
    place_of_birth_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.place_of_birth"]),
        help_text=_(TXT["author.place_of_birth_cs.help"]),
    )
    i18n_place_of_birth = TranslatedField.named("place_of_birth", True)

    date_of_death_year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        verbose_name=_(TXT["author.date_of_death_year"]),
        help_text=_(TXT["author.date_of_death_year.help"]),
    )
    date_of_death_month = models.PositiveSmallIntegerField(
        choices=dates.MONTHS.items(),
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name=_(TXT["author.date_of_death_month"]),
        help_text=_(TXT["author.date_of_death_month.help"]),
    )
    date_of_death_day = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        verbose_name=_(TXT["author.date_of_death_day"]),
        help_text=_(TXT["author.date_of_death_day.help"]),
    )
    place_of_death = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.place_of_death"]),
        help_text=_(TXT["author.place_of_death.help"]),
    )
    place_of_death_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.place_of_death"]),
        help_text=_(TXT["author.place_of_death_de.help"]),
    )
    place_of_death_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.place_of_death"]),
        help_text=_(TXT["author.place_of_death_cs.help"]),
    )
    i18n_place_of_death = TranslatedField.named("place_of_death", True)

    language_tags = ParentalManyToManyField(
        "LanguageTag",
        db_table=DB_TABLE_PREFIX + "author_tag_language",
        related_name="authors",
        blank=True,
        verbose_name=_(TXT["author.language.plural"]),
        help_text=_(TXT["author.language.help"]),
    )
    genre_tags = ParentalManyToManyField(
        "GenreTag",
        db_table=DB_TABLE_PREFIX + "author_tag_genre",
        related_name="authors",
        blank=True,
        verbose_name=_(TXT["author.genre.plural"]),
        help_text=_(TXT["author.genre.help"]),
    )
    literary_period_tags = ParentalManyToManyField(
        "PeriodTag",
        db_table=DB_TABLE_PREFIX + "author_tag_literary_period",
        related_name="authors",
        blank=True,
        verbose_name=_(TXT["author.literary_period.plural"]),
        help_text=_(TXT["author.literary_period.help"]),
    )

    @property
    def born(self):
        """Return the year of birth as a datetime object."""
        if (
            self.date_of_birth_year
            and self.date_of_birth_month
            and self.date_of_birth_day
        ):
            return datetime.date(
                self.date_of_birth_year,
                self.date_of_birth_month,
                self.date_of_birth_day,
            )

    @property
    def died(self):
        """Return the year of death as a datetime object."""
        if (
            self.date_of_death_year
            and self.date_of_death_month
            and self.date_of_death_day
        ):
            return datetime.date(
                self.date_of_death_year,
                self.date_of_death_month,
                self.date_of_death_day,
            )

    @property
    def age(self):
        """Return the age of the author in years."""
        if self.born and self.died:
            diff_year = self.died.year - self.born.year
            diff_remainder = (self.died.month, self.died.day) < (
                self.born.month,
                self.born.day,
            )
            return diff_year - diff_remainder

    parent_page_types = ["AuthorIndex"]
    search_fields = Page.search_fields + [
        index.RelatedFields(
            "names",
            [
                index.SearchField("title"),
                index.SearchField("first_name"),
                index.SearchField("last_name"),
                index.FilterField("birth_name"),
                index.FilterField("is_pseudonym"),
            ],
        ),
        index.FilterField("sex"),
        index.FilterField("born"),
        index.FilterField("died"),
        index.FilterField("age"),
    ]
    general_panels = [
        ImageChooserPanel("title_image"),
        InlinePanel(
            "names",
            panels=[
                FieldPanel("is_pseudonym"),
                FieldPanelTabs(
                    children=[
                        MultiFieldPanel(
                            children=[
                                FieldPanel("title"),
                                FieldPanel("first_name"),
                                FieldPanel("last_name"),
                                FieldPanel("birth_name"),
                            ],
                            heading=_(TXT["heading.en"]),
                            classname="collapsible",
                        ),
                        MultiFieldPanel(
                            children=[
                                FieldPanel("title_de"),
                                FieldPanel("first_name_de"),
                                FieldPanel("last_name_de"),
                                FieldPanel("birth_name_de"),
                            ],
                            heading=_(TXT["heading.de"]),
                        ),
                        MultiFieldPanel(
                            children=[
                                FieldPanel("title_cs"),
                                FieldPanel("first_name_cs"),
                                FieldPanel("last_name_cs"),
                                FieldPanel("birth_name_cs"),
                            ],
                            heading=_(TXT["heading.cs"]),
                        ),
                    ],
                    heading=_(TXT["author.name"]),
                ),
            ],
            label=_(TXT["author.name.plural"]),
            min_num=1,
            help_text=_(TXT["author.name.help"]),
        ),
        FieldPanel("sex"),
        MultiFieldPanel(
            children=[
                FieldPanel("date_of_birth_day"),
                FieldPanel("date_of_birth_month"),
                FieldPanel("date_of_birth_year"),
                FieldPanelTabs(
                    children=[
                        FieldPanelTab("place_of_birth", heading=_(TXT["language.en"])),
                        FieldPanelTab(
                            "place_of_birth_de", heading=_(TXT["language.de"])
                        ),
                        FieldPanelTab(
                            "place_of_birth_cs", heading=_(TXT["language.cs"])
                        ),
                    ],
                    heading=_(TXT["author.place_of_birth"]),
                ),
            ],
            heading=_(TXT["author.date_of_birth"]),
        ),
        MultiFieldPanel(
            children=[
                FieldPanel("date_of_death_day"),
                FieldPanel("date_of_death_month"),
                FieldPanel("date_of_death_year"),
                FieldPanelTabs(
                    children=[
                        FieldPanelTab("place_of_death", heading=_(TXT["language.en"])),
                        FieldPanelTab(
                            "place_of_death_de", heading=_(TXT["language.de"])
                        ),
                        FieldPanelTab(
                            "place_of_death_cs", heading=_(TXT["language.cs"])
                        ),
                    ],
                    heading=_(TXT["author.place_of_death"]),
                ),
            ],
            heading=_(TXT["author.date_of_death"]),
        ),
        MultiFieldPanel(
            heading=_(TXT["tag.plural"]),
            children=[
                FieldPanel(
                    field_name="language_tags",
                    widget=autocomplete.ModelSelect2Multiple(
                        url="autocomplete-language"
                    ),
                ),
                FieldPanel(
                    field_name="genre_tags",
                    widget=autocomplete.ModelSelect2Multiple(url="autocomplete-genre"),
                ),
                FieldPanel(
                    field_name="literary_period_tags",
                    widget=autocomplete.ModelSelect2Multiple(
                        url="autocomplete-literary-period"
                    ),
                ),
            ],
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(general_panels, heading=_(TXT["heading.general"])),
            ObjectList(I18nPage.meta_panels, heading=_(TXT["heading.meta"])),
        ]
    )

    @property
    def full_name_title(self):
        """Return the full name of the author including her birth name to be used in titles."""
        return self.names.first().full_name_title(self.sex)

    @property
    def formatted_date_of_birth(self):
        """Format date of birth in human readable string."""
        return format_date(
            self.date_of_birth_year, self.date_of_birth_month, self.date_of_birth_day
        )

    @property
    def formatted_date_of_death(self):
        """Format date of death in human readable string."""
        return format_date(
            self.date_of_death_year, self.date_of_death_month, self.date_of_death_day
        )

    def full_clean(self, *args, **kwargs):
        """Add autogenerated values for non-editable required fields."""
        name = self.names.first()
        if name:
            self.title = name.full_name()
            self.title_de = name.full_name_de()
            self.title_cs = name.full_name_cs()
            base_slug = text.slugify(name.last_name, allow_unicode=True)
            self.slug = self._get_autogenerated_slug(base_slug)

        super(Author, self).full_clean(*args, **kwargs)

    def clean(self):
        """Validate date components of input."""
        super(Author, self).clean()
        validate_date(
            self.date_of_birth_year, self.date_of_birth_month, self.date_of_birth_day
        )
        validate_date(
            self.date_of_death_year, self.date_of_death_month, self.date_of_death_day
        )

    def get_context(self, request, *args, **kwargs):
        """Add more context information on view requests."""
        context = super(Author, self).get_context(request, *args, **kwargs)
        author = self.get_latest_revision_as_page() if request.is_preview else self
        context["author"] = author

        # add all names of author to context
        context["author_name"], *context["author_alt_names"] = author.names.order_by(
            "sort_order"
        )

        # add level pages
        levels = self.get_children().specific()
        if request.is_preview:
            levels = [x.get_latest_revision_as_page() for x in levels]
        else:
            levels = levels.live()
        context["levels"] = sorted(levels, key=lambda x: x.level_order)

        # add memorial sites
        memorial_sites = Memorial.objects.filter(authors__author=self)
        if request.is_preview:
            memorial_sites = [x.get_latest_revision_as_page() for x in memorial_sites]
        else:
            memorial_sites = memorial_sites.live()
        context["memorial_sites"] = memorial_sites

        return context

    class Meta:
        db_table = DB_TABLE_PREFIX + "author"
        verbose_name = _(TXT["author"])
        verbose_name_plural = _(TXT["author.plural"])


class AuthorName(Orderable):
    """A join relation that holds the name of an author."""

    author = ParentalKey("Author", related_name="names")

    is_pseudonym = models.BooleanField(
        default=False,
        verbose_name=_(TXT["author.name.is_pseudonym"]),
        help_text=_(TXT["author.name.is_pseudonym.help"]),
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.title"]),
        help_text=_(TXT["author.name.title.help"]),
    )
    title_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.title"]),
        help_text=_(TXT["author.name.title_de.help"]),
    )
    title_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.title"]),
        help_text=_(TXT["author.name.title_cs.help"]),
    )
    i18n_title = TranslatedField.named("title", True)

    first_name = models.CharField(
        max_length=255, blank=True, verbose_name=_(TXT["author.name.first_name"])
    )
    first_name_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.first_name"]),
        help_text=_(TXT["author.name.first_name_de.help"]),
    )
    first_name_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.first_name"]),
        help_text=_(TXT["author.name.first_name_cs.help"]),
    )
    i18n_first_name = TranslatedField.named("first_name", True)

    last_name = models.CharField(
        max_length=255, verbose_name=_(TXT["author.name.last_name"])
    )
    last_name_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.last_name"]),
        help_text=_(TXT["author.name.last_name_de.help"]),
    )
    last_name_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.last_name"]),
        help_text=_(TXT["author.name.last_name_cs.help"]),
    )
    i18n_last_name = TranslatedField.named("last_name", True)

    birth_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.birth_name"]),
        help_text=_(TXT["author.name.birth_name.help"]),
    )
    birth_name_de = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.birth_name"]),
        help_text=_(TXT["author.name.birth_name_de.help"]),
    )
    birth_name_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["author.name.birth_name"]),
        help_text=_(TXT["author.name.birth_name_cs.help"]),
    )
    i18n_birth_name = TranslatedField.named("birth_name", True)

    def full_name_title(self, gender=Author.GENDER_MALE):
        """Return the full name of this name object formatted to include the birth name."""
        name = str(self)
        birth_name = self.i18n_birth_name
        if birth_name:
            if gender == Author.GENDER_FEMALE:
                addendum = pgettext("female", f"born {birth_name}")
            else:
                addendum = pgettext("male", f"born {birth_name}")
            name += f" ({addendum})"
        return name

    def clean(self):
        """Check wether any valid name has been set."""
        super(AuthorName, self).clean()
        if not self.first_name and not self.last_name:
            message = _(TXT["author.name.validation"])
            raise ValidationError(message)

    def full_name(self):
        """Return the full name of the author in english language."""
        return " ".join(
            x.strip() for x in [self.title, self.first_name, self.last_name] if x
        )

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

    class Meta:
        db_table = DB_TABLE_PREFIX + "author_name"
        verbose_name = _(TXT["author_name"])
        verbose_name_plural = _(TXT["author_name.plural"])


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


class Memorial(I18nPage):
    """A geographic place on earth."""

    template = "cms/memorial_site.html"
    parent_page_types = ["LocationIndex"]

    title_image = models.ForeignKey(
        "ImageMedia",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_(TXT["memorial_site.title_image"]),
        help_text=_(TXT["memorial_site.title_image.help"]),
    )
    memorial_type_tags = ParentalManyToManyField(
        "MemorialTag",
        db_table=DB_TABLE_PREFIX + "memorial_site_tag_memorial_type",
        related_name="memorial_site",
        blank=False,
        verbose_name=_(TXT["memorial_site.memorial_type_tags.plural"]),
        help_text=_(TXT["memorial_site.memorial_type_tags.help"]),
    )

    address = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["memorial_site.address"]),
        help_text=_(TXT["memorial_site.address.help"]),
    )
    address_de = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["memorial_site.address"]),
        help_text=_(TXT["memorial_site.address.help"]),
    )
    address_cs = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["memorial_site.address"]),
        help_text=_(TXT["memorial_site.address.help"]),
    )
    i18n_address = TranslatedField.named("address", True)

    contact_info = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["memorial_site.contact_info"]),
        help_text=_(TXT["memorial_site.contact_info.help"]),
    )
    contact_info_de = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["memorial_site.contact_info"]),
        help_text=_(TXT["memorial_site.contact_info.help"]),
    )
    contact_info_cs = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["memorial_site.contact_info"]),
        help_text=_(TXT["memorial_site.contact_info.help"]),
    )
    i18n_contact_info = TranslatedField.named("contact_info", True)

    directions = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["memorial_site.directions"]),
        help_text=_(TXT["memorial_site.directions.help"]),
    )
    directions_de = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["memorial_site.directions"]),
        help_text=_(TXT["memorial_site.directions.help"]),
    )
    directions_cs = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["memorial_site.directions"]),
        help_text=_(TXT["memorial_site.directions.help"]),
    )
    i18n_directions = TranslatedField.named("directions")

    coordinates = PointField(
        verbose_name=_(TXT["memorial_site.coordinates"]),
        help_text=_(TXT["memorial_site.coordinates.help"]),
    )

    introduction = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["memorial_site.introduction"]),
        help_text=_(TXT["memorial_site.introduction.help"]),
    )
    introduction_de = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["memorial_site.introduction"]),
        help_text=_(TXT["memorial_site.introduction.help"]),
    )
    introduction_cs = RichTextField(
        blank=True,
        features=I18nPage.RICH_TEXT_FEATURES,
        verbose_name=_(TXT["memorial_site.introduction"]),
        help_text=_(TXT["memorial_site.introduction.help"]),
    )
    i18n_introduction = TranslatedField.named("introduction")

    description = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["memorial_site.description"]),
        help_text=_(TXT["memorial_site.description.help"]),
    )
    description_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["memorial_site.description"]),
        help_text=_(TXT["memorial_site.description.help"]),
    )
    description_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["memorial_site.description"]),
        help_text=_(TXT["memorial_site.description.help"]),
    )
    i18n_description = TranslatedField.named("description")

    detailed_description = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["memorial_site.detailed_description"]),
        help_text=_(TXT["memorial_site.detailed_description.help"]),
    )
    detailed_description_de = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["memorial_site.detailed_description"]),
        help_text=_(TXT["memorial_site.detailed_description.help"]),
    )
    detailed_description_cs = StreamField(
        [("paragraph", ParagraphStructBlock())],
        blank=True,
        verbose_name=_(TXT["memorial_site.detailed_description"]),
        help_text=_(TXT["memorial_site.detailed_description.help"]),
    )
    i18n_detailed_description = TranslatedField.named("detailed_description")

    search_fields = I18nPage.search_fields + [
        index.SearchField("directions"),
        index.SearchField("directions_de"),
        index.SearchField("directions_cs"),
    ]

    general_panels = [
        ImageChooserPanel("title_image"),
        FieldPanel(
            "memorial_type_tags",
            widget=autocomplete.ModelSelect2Multiple(
                url="autocomplete-location-type",
                attrs={"data-maximum-selection-length": 1},
            ),
        ),
        InlinePanel(
            "authors",
            label=_(TXT["memorial_site.authors"]),
            min_num=1,
            help_text=_(TXT["memorial_site.authors"]),
            panels=[PageChooserPanel("author", "cms.Author")],
        ),
        FieldPanelTabs(
            children=[
                FieldPanelTab("address", heading=_(TXT["language.en"])),
                FieldPanelTab("address_de", heading=_(TXT["language.de"])),
                FieldPanelTab("address_cs", heading=_(TXT["language.cs"])),
            ],
            heading=_(TXT["memorial_site.address"]),
            show_label=False,
        ),
        FieldPanelTabs(
            children=[
                FieldPanelTab("contact_info", heading=_(TXT["language.en"])),
                FieldPanelTab("contact_info_de", heading=_(TXT["language.de"])),
                FieldPanelTab("contact_info_cs", heading=_(TXT["language.cs"])),
            ],
            heading=_(TXT["memorial_site.contact_info"]),
            show_label=False,
        ),
        FieldPanelTabs(
            children=[
                FieldPanelTab("directions", heading=_(TXT["language.en"])),
                FieldPanelTab("directions_de", heading=_(TXT["language.de"])),
                FieldPanelTab("directions_cs", heading=_(TXT["language.cs"])),
            ],
            heading=_(TXT["memorial_site.directions"]),
            show_label=False,
        ),
        FieldPanel("coordinates", widget=GooglePointFieldWidget()),
    ]
    english_panels = I18nPage.english_panels + [
        FieldPanel("introduction"),
        StreamFieldPanel("description"),
        StreamFieldPanel("detailed_description"),
    ]
    german_panels = I18nPage.german_panels + [
        FieldPanel("introduction_de"),
        StreamFieldPanel("description_de"),
        StreamFieldPanel("detailed_description_de"),
    ]
    czech_panels = I18nPage.czech_panels + [
        FieldPanel("introduction_cs"),
        StreamFieldPanel("description_cs"),
        StreamFieldPanel("detailed_description_cs"),
    ]
    meta_panels = I18nPage.meta_panels + [FieldPanel("slug")]
    edit_handler = TabbedInterface(
        [
            ObjectList(general_panels, heading=_(TXT["heading.general"])),
            ObjectList(english_panels, heading=_(TXT["heading.en"])),
            ObjectList(german_panels, heading=_(TXT["heading.de"])),
            ObjectList(czech_panels, heading=_(TXT["heading.cs"])),
            ObjectList(meta_panels, heading=_(TXT["heading.meta"])),
        ]
    )

    class Meta:
        db_table = DB_TABLE_PREFIX + "memorial"
        verbose_name = _(TXT["memorial"])
        verbose_name_plural = _(TXT["memorial.plural"])


class LocationAuthor(Orderable):
    """Join page type to add multiple authors to one memorial site."""

    memorial_site = ParentalKey(
        "Memorial",
        related_name="authors",
        verbose_name=_(TXT["memorial_site_author.memorial_site"]),
        help_text=_(TXT["memorial_site_author.memorial_site.help"]),
    )
    author = models.ForeignKey(
        "Author",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="locations",
        verbose_name=_(TXT["memorial_site_author.author"]),
        help_text=_(TXT["memorial_site_author.author.help"]),
    )

    class Meta:
        db_table = DB_TABLE_PREFIX + "memorial_site_author"
        verbose_name = _(TXT["memorial_site_author"])
        verbose_name_plural = _(TXT["memorial_site_author.plural"])
