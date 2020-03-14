"""Custom hooks to add functionality to the Wagtail framework."""

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    BlockElementHandler,
    InlineStyleElementHandler,
)
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.core import hooks
from wagtail.core.models import PageRevision

from cms.models import Author
from .models import (
    AgeGroupTag,
    GenreTag,
    I18nPage,
    LanguageTag,
    PeriodTag,
    MemorialTag,
)


def as_page_object(self):
    """Return the PageRevision as a specific Page class."""
    obj = self.page.specific_class.from_json(self.content_json)
    specific_page = self.page.specific

    # Override the possibly-outdated tree parameter fields from this revision object
    # with up-to-date values
    obj.pk = self.page.pk
    obj.path = self.page.path
    obj.depth = self.page.depth
    obj.numchild = self.page.numchild

    # Populate url_path based on the revision"s current slug and the parent page as determined
    # by path
    obj.set_url_path(self.page.get_parent())

    # also copy over other properties which are meaningful for the page as a whole, not a
    # specific revision of it
    obj.draft_title = self.page.draft_title

    # copy over properties that are derievied from our custom i18n class
    if isinstance(obj, I18nPage):
        obj.draft_title_de = specific_page.draft_title_de
        obj.draft_title_cs = specific_page.draft_title_cs
    elif isinstance(obj, Author):
        author_name = specific_page.names.order_by("sort_order").first()
        obj.draft_title = author_name.full_name()
        obj.draft_title_de = author_name.full_name_de()
        obj.draft_title_cs = author_name.full_name_cs()

    obj.live = self.page.live
    obj.has_unpublished_changes = self.page.has_unpublished_changes
    obj.owner = self.page.owner
    obj.locked = self.page.locked
    obj.latest_revision_created_at = self.page.latest_revision_created_at
    obj.first_published_at = self.page.first_published_at

    return obj


# Patches the Wagtail PageRevision to work with our custom i18n implementation
PageRevision.as_page_object = as_page_object


@hooks.register("insert_global_admin_js")
def global_admin_js():
    """Add custom JavaScript logic to the admin."""
    return format_html("<script defer src='{}'></script>", static("fontawesome-custom.js"))


@hooks.register("register_rich_text_features")
def register_strikethrough_feature(features):
    """Register the `strikethrough` editor feature."""
    feature_name = "strikethrough"
    type_ = "STRIKETHROUGH"
    tag = "s"

    control = {
        "type": type_,
        "icon": " fas fa-strikethrough",
        "description": gettext("Strikethrough"),
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: tag}},
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)


@hooks.register("register_rich_text_features")
def register_footnote_feature(features):
    """Register the `footnote` editor feature."""
    feature_name = "footnote"
    type_ = "FOOTNOTE"
    tag = "span"

    control = {
        "type": type_,
        "icon": " fas fa-sticky-note",
        "description": gettext("Footnote"),
        "class": "footnote",
        "style": {
            "backgroundColor": "#e6e6e6",
            "border": "1px solid #333",
            "fontFamily": "monospace",
            "fontWeight": "bold",
            "marginLeft": ".1rem",
            "padding": ".1rem",
        },
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {
            "style_map": {type_: {"element": tag, "props": {"class": "footnote"}}}
        },
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)


@hooks.register("register_rich_text_features")
def register_blockquote_feature(features):
    """Register the `blockquote` feature using the `blockquote` Draft.js block type."""
    feature_name = "blockquote"
    type_ = "BLOCKQUOTE"
    tag = "blockquote"

    control = {
        "type": type_,
        "icon": " fas fa-quote-right",
        "description": gettext("Blockquote"),
        "element": "blockquote",
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.BlockFeature(control)
    )

    features.register_converter_rule(
        "contentstate",
        feature_name,
        {
            "from_database_format": {tag: BlockElementHandler(type_)},
            "to_database_format": {
                "block_map": {
                    type_: {"element": tag, "props": {"class": "blockquote text-right"}}
                }
            },
        },
    )


class TagModelAdmin(ModelAdmin):
    """Generic tag admin class."""

    list_display = ("title", "title_de", "title_cs")
    search_fields = ("title", "title_de", "title_cs")


class GenreModelAdmin(TagModelAdmin):
    """Genre tag model admin."""

    model = GenreTag
    menu_icon = "pilcrow"


class LanguageModelAdmin(TagModelAdmin):
    """Language tag model admin."""

    model = LanguageTag
    menu_icon = "openquote"


class LocationTypeModelAdmin(TagModelAdmin):
    """Location type tag model admin."""

    model = MemorialTag
    menu_icon = "site"


class LiteraryPeriodModelAdmin(TagModelAdmin):
    """Literary period tag model admin."""

    list_display = TagModelAdmin.list_display + ("sort_order",)
    model = PeriodTag
    menu_icon = "date"


class AgeGroupModelAdmin(TagModelAdmin):
    """Age group tag model admin."""

    list_display = TagModelAdmin.list_display + ("sort_order",)
    model = AgeGroupTag
    menu_icon = "group"


class TagGroup(ModelAdminGroup):
    """Tag group that groups all domain tag models."""

    menu_label = _("Tags")
    menu_icon = "tag"
    menu_order = 200
    items = (
        GenreModelAdmin,
        LanguageModelAdmin,
        LocationTypeModelAdmin,
        LiteraryPeriodModelAdmin,
        AgeGroupModelAdmin,
    )


modeladmin_register(TagGroup)
