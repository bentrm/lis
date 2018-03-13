import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler, BlockElementHandler
from wagtail.core import hooks
from wagtail.core.models import PageRevision

from cms.models import I18nPage, AuthorPage


def as_page_object(self):
    obj = self.page.specific_class.from_json(self.content_json)
    specific_page = self.page.specific

    # Override the possibly-outdated tree parameter fields from this revision object
    # with up-to-date values
    obj.pk = self.page.pk
    obj.path = self.page.path
    obj.depth = self.page.depth
    obj.numchild = self.page.numchild

    # Populate url_path based on the revision's current slug and the parent page as determined
    # by path
    obj.set_url_path(self.page.get_parent())

    # also copy over other properties which are meaningful for the page as a whole, not a
    # specific revision of it
    obj.draft_title = self.page.draft_title

    # copy over properties that are derievied from out custom i18n class
    if isinstance(obj, I18nPage):
        obj.draft_title_de = specific_page.draft_title_de
        obj.draft_title_cz = specific_page.draft_title_cz
    elif isinstance(obj, AuthorPage):
        author_name = specific_page.names.first()
        obj.draft_title = author_name.full_name()
        obj.draft_title_de = author_name.full_name_de()
        obj.draft_title_cz = author_name.full_name_cz()

    obj.live = self.page.live
    obj.has_unpublished_changes = self.page.has_unpublished_changes
    obj.owner = self.page.owner
    obj.locked = self.page.locked
    obj.latest_revision_created_at = self.page.latest_revision_created_at
    obj.first_published_at = self.page.first_published_at

    return obj


# Patches the Wagtail PageRevision to work with our custom i18n implementation
PageRevision.as_page_object = as_page_object

# from .models import TextType, ContactType, LiteraryPeriod, LiteraryCategory
#
#
# class LiteraryPeriodModelAdmin(ModelAdmin):
#     model = LiteraryPeriod
#     menu_icon = "time"
#     menu_order = 500
#     list_display = ("__str__",)
#     search_fields = ("name",)
#
#
# class LiteraryCategoryModelAdmin(ModelAdmin):
#     model = LiteraryCategory
#     menu_icon = "tag"
#     menu_order = 501
#     list_display = ("name", "description", "sort_order",)
#     search_fields = ("name", "description",)
#
#
# class TextTypeModelAdmin(ModelAdmin):
#     model = TextType
#     menu_icon = "pilcrow"
#     menu_order = 502
#     list_display = ("name",)
#     search_fields = ("name",)
#
#
# class ContactTypeModelAdmin(ModelAdmin):
#     model = ContactType
#     menu_icon = "mail"
#     menu_order = 503
#     list_display = ("name",)
#     search_fields = ("name",)
#
#
# modeladmin_register(LiteraryPeriodModelAdmin)
# modeladmin_register(LiteraryCategoryModelAdmin)
# modeladmin_register(TextTypeModelAdmin)
# modeladmin_register(ContactTypeModelAdmin)


@hooks.register('register_rich_text_features')
def register_strikethrough_feature(features):
    """
    Registering the `strikethrough` feature, which uses the `STRIKETHROUGH` Draft.js inline style type,
    and is stored as HTML with an `<s>` tag.
    """
    feature_name = 'strikethrough'
    type_ = 'STRIKETHROUGH'
    tag = 's'

    control = {
        'type': type_,
        'label': 'S',
        'icon': 'fas fa-strikethrough',
        'description': 'Strikethrough',
        # This isn’t even required – Draftail has predefined styles for STRIKETHROUGH.
        # 'style': {'textDecoration': 'line-through'},
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: tag}},
    }

    features.register_converter_rule('contentstate', feature_name, db_conversion)


@hooks.register('register_rich_text_features')
def register_strikethrough_feature(features):
    feature_name = 'sup'
    type_ = 'SUPERSCRIPT'
    tag = 'sup'

    control = {
        'type': type_,
        'label': 'sup',
        'icon': 'fas fa-superscript',
        'description': 'Superscript'
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: tag}},
    }

    features.register_converter_rule('contentstate', feature_name, db_conversion)


@hooks.register('register_rich_text_features')
def register_blockquote_feature(features):
    """
    Registering the `blockquote` feature, which uses the `blockquote` Draft.js block type,
    and is stored as HTML with a `<blockquote>` tag.
    """
    feature_name = 'blockquote'
    type_ = 'blockquote'
    tag = 'blockquote'

    control = {
        'type': type_,
        'label': '❝',
        'description': 'Blockquote',
        # Optionally, we can tell Draftail what element to use when displaying those blocks in the editor.
        'element': 'blockquote',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control)
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {tag: BlockElementHandler(type_)},
        'to_database_format': {'block_map': {type_: tag}},
    })
