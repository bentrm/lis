from dal import autocomplete
from django.contrib.gis.db.models import PointField
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, TabbedInterface, ObjectList
from wagtail.api import APIField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from cms.blocks import ParagraphStructBlock
from cms.edit_handlers import FieldPanelTabs, FieldPanelTab
from cms.messages import TXT
from cms.widgets import CustomGooglePointFieldWidget
from .base import CategoryPage, DB_TABLE_PREFIX, I18nPage, TranslatedField


class LocationIndex(RoutablePageMixin, CategoryPage):
    """A category page to place locations in."""

    parent_page_types = ["HomePage"]
    template = "cms/preview/blog.html"

    @route(r'^$')
    def serve_base_map(self, request):
        """
        View function for the current events page
        """
        return self.serve(request)

    @route(r'^@.*$')
    def serve_positioned_base_map(self, request):
        return self.serve(request)

    class Meta:
        db_table = DB_TABLE_PREFIX + "locations"
        verbose_name = _(TXT["location.plural"])


class Memorial(I18nPage):
    """A geographic place on earth."""

    template = "cms/preview/memorial.html"
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

    remembered_authors = ParentalManyToManyField(
        "Author",
        # db_table=DB_TABLE_PREFIX + "memorial_author",
        related_name="memorials",
        blank=False,
        verbose_name=_(TXT["memorial_site.authors"]),
        help_text=_(TXT["memorial_site.authors.help"]),
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
        index.SearchField("address"),
        index.SearchField("address_de"),
        index.SearchField("address_cs"),
        index.SearchField("contact_info"),
        index.SearchField("contact_info_de"),
        index.SearchField("contact_info_cs"),
        index.SearchField("directions"),
        index.SearchField("directions_de"),
        index.SearchField("directions_cs"),
        index.SearchField("introduction"),
        index.SearchField("introduction_de"),
        index.SearchField("introduction_cs"),
        index.SearchField("description"),
        index.SearchField("description_de"),
        index.SearchField("description_cs"),
        index.SearchField("detailed_description"),
        index.SearchField("detailed_description_de"),
        index.SearchField("detailed_description_cs"),
        index.FilterField("remembered_authors"),
        index.FilterField("memorial_type_tags"),
        index.FilterField("coordinates"),
    ]

    api_fields = I18nPage.api_fields + [
        APIField("title_image"),
        APIField("remembered_authors"),
        APIField("memorial_type_tags"),
        APIField("address"),
        APIField("address_de"),
        APIField("address_cs"),
        APIField("contact_info"),
        APIField("contact_info_de"),
        APIField("contact_info_cs"),
        APIField("directions"),
        APIField("directions_de"),
        APIField("directions_cs"),
        APIField("introduction"),
        APIField("introduction_de"),
        APIField("introduction_cs"),
        APIField("description"),
        APIField("description_de"),
        APIField("description_cs"),
        APIField("detailed_description"),
        APIField("detailed_description_de"),
        APIField("detailed_description_cs"),
        APIField("coordinates"),
    ]

    general_panels = [
        ImageChooserPanel("title_image"),
        FieldPanel(
            "memorial_type_tags",
            widget=autocomplete.ModelSelect2Multiple(
                url="autocomplete-location-type",
            ),
        ),
        FieldPanel(
            "remembered_authors",
            widget=autocomplete.ModelSelect2Multiple(
                url="autocomplete-author",
            ),
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
        FieldPanel("coordinates", widget=CustomGooglePointFieldWidget()),
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

    class JSONAPIMeta:
        resource_name = 'memorials'
