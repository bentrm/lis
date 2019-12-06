from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, TabbedInterface, ObjectList, InlinePanel, \
    PageChooserPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable
from wagtail.search import index

from cms.edit_handlers import FieldPanelTabs, FieldPanelTab
from cms.messages import TXT
from cms.models import CategoryPage, DB_TABLE_PREFIX, I18nPage, TranslatedField


class MemorialPathIndex(CategoryPage):
    """Route category page."""

    parent_page_types = ['HomePage']
    template = "cms/preview/blog.html"

    class Meta:
        db_table = DB_TABLE_PREFIX + 'memorial_memorial_paths'
        verbose_name = _(TXT['memorial_path.plural'])


class MemorialPath(I18nPage):
    """A list of memorials."""

    parent_page_types = ['MemorialPathIndex']

    description = RichTextField(
        features=I18nPage.RICH_TEXT_FEATURES,
        blank=True,
        verbose_name=_(TXT['memorial_path.description']),
        help_text=_(TXT['memorial_path.description.help']),
    )
    description_de = RichTextField(
        features=I18nPage.RICH_TEXT_FEATURES,
        blank=True,
        verbose_name=_(TXT['memorial_path.description']),
        help_text=_(TXT['memorial_path.description.help']),
    )
    description_cs = RichTextField(
        features=I18nPage.RICH_TEXT_FEATURES,
        blank=True,
        verbose_name=_(TXT['memorial_path.description']),
        help_text=_(TXT['memorial_path.description.help']),
    )
    i18n_description = TranslatedField.named('description')

    search_fields = I18nPage.search_fields + [
        index.SearchField('description'),
        index.SearchField('description_de'),
        index.SearchField('description_cs'),
    ]

    api_fields = I18nPage.api_fields + [
        APIField('description'),
        APIField('description_de'),
        APIField('description_cs'),
    ]

    general_panels = [
        FieldPanelTabs(
            children=[
                FieldPanelTab('title', heading=_(TXT['language.en'])),
                FieldPanelTab('title_de', heading=_(TXT['language.de'])),
                FieldPanelTab('title_cs', heading=_(TXT['language.cs'])),
            ],
            heading=_(TXT['page.title'])
        ),
        FieldPanelTabs(
            children=[
                FieldPanelTab('description', heading=_(TXT['language.en'])),
                FieldPanelTab('description_de', heading=_(TXT['language.de'])),
                FieldPanelTab('description_cs', heading=_(TXT['language.cs'])),
            ],
            heading=_(TXT['memorial_path.description'])
        ),
        MultiFieldPanel(
            children=[
                InlinePanel('waypoints', panels=[
                    PageChooserPanel('memorial'),
                ]),
            ],
            heading=_(TXT['memorial_path_waypoint.plural'])
        ),
    ]
    meta_panels = I18nPage.meta_panels + [
        FieldPanel("slug")
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(general_panels, heading=_(TXT["heading.general"])),
            ObjectList(meta_panels, heading=_(TXT["heading.meta"])),
        ]
    )

    class Meta:
        db_table = DB_TABLE_PREFIX + 'memorial_path'
        verbose_name = _(TXT['memorial_path'])
        verbose_name_plural = _(TXT['memorial_path.plural'])


class Waypoint(Orderable):

    memorial_path = ParentalKey('cms.MemorialPath', related_name='waypoints', verbose_name=_(TXT['memorial_path']))
    memorial = ParentalKey('cms.Memorial', related_name='memorial_memorial_paths', verbose_name=_(TXT['memorial']))

    class Meta:
        db_table = DB_TABLE_PREFIX + 'memorial_path_waypoint'
        verbose_name = _(TXT['memorial_path_waypoint'])
        verbose_name_plural = _(TXT['memorial_path_waypoint.plural'])
