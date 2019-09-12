import datetime

from dal import autocomplete
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import dates, text
from django.utils.translation import gettext_lazy as _, pgettext
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from wagtail.admin.edit_handlers import InlinePanel, FieldPanel, MultiFieldPanel, TabbedInterface, ObjectList
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from cms.edit_handlers import FieldPanelTabs, FieldPanelTab
from cms.messages import TXT
from .base import CategoryPage, DB_TABLE_PREFIX, I18nPage, TranslatedField
from .helpers import validate_date, format_date
from .memorial import Memorial


class AuthorIndex(CategoryPage):
    """A category page to place author pages in."""

    parent_page_types = ["HomePage"]
    template = "app/author-list.html"

    class Meta:
        db_table = DB_TABLE_PREFIX + "authors"
        verbose_name = _(TXT["author.plural"])


class Author(I18nPage):
    """A page that describes an author."""

    template = "app/author-detail.html"

    GENDER_UNKNOWN = "U"
    GENDER_MALE = "M"
    GENDER_FEMALE = "F"
    GENDER_CHOICES = (
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
        choices=list(dates.MONTHS.items()),
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
        choices=list(dates.MONTHS.items()),
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
    search_fields = I18nPage.search_fields + [
        index.RelatedFields(
            "names",
            [
                index.SearchField("title"),
                index.SearchField("first_name"),
                index.SearchField("last_name"),
                index.SearchField("birth_name"),
                index.FilterField("is_pseudonym"),
            ],
        ),
        index.FilterField("sex"),
        index.FilterField("genretag_id"),
        index.FilterField("languagetag_id"),
        index.FilterField("literaryperiod_id"),
        index.FilterField("born"),
        index.FilterField("died"),
        index.FilterField("age"),
    ]
    api_fields = I18nPage.api_fields + [
        "sex",
        "genre_tags",
        "genretag_id",
        "language_tags",
        "literary_period_tags",
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
            levels = levels.public().live()

        context["levels"] = sorted(levels, key=lambda x: x.level_order)

        # add memorial sites
        memorial_sites = Memorial.objects.filter(remembered_authors=self)
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

    class JSONAPIMeta:
        resource_name = "authors"


class AuthorName(Orderable):
    """A join relation that holds the name of an author."""

    author = ParentalKey("cms.Author", related_name="names")

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

    class JSONAPIMeta:
        resource_name = "names"
