"""Base model classes and constants."""

import logging
from collections import namedtuple
from typing import NewType, Tuple

from django.core.exceptions import PermissionDenied
from django.db import models
from django.shortcuts import redirect
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import (
    FieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core.blocks import CharBlock, RichTextBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import BaseViewRestriction, Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index

from .helpers import TranslatedField
from ..messages import TXT

LOGGER = logging.getLogger("cms.models")
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

TextType = namedtuple("TextType", ["field", "heading"])


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
        help_text=_(TXT["page.title_de.help"]),
    )
    title_cs = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_(TXT["page.title_cs"]),
        help_text=_(TXT["page.title_cs.help"]),
    )
    i18n_title = TranslatedField.named("title", True)

    draft_title_de = models.CharField(
        max_length=255,
        blank=True,
        editable=False,
        verbose_name=_(TXT["page.draft_title_de"]),
        help_text=_(TXT["page.draft_title_de.help"]),
    )
    draft_title_cs = models.CharField(
        max_length=255,
        blank=True,
        editable=False,
        verbose_name=_(TXT["page.draft_title_cs"]),
        help_text=_(TXT["page.draft_title_cs.help"]),
    )
    i18n_draft_title = TranslatedField.named("draft_title", True)

    editor = models.CharField(
        max_length=2048,
        verbose_name=_(TXT["page.editor"]),
        help_text=_(TXT["page.editor.help"]),
    )
    original_language = models.CharField(
        max_length=3,
        choices=ORIGINAL_LANGUAGE,
        default=ORIGINAL_LANGUAGE_GERMAN,
        verbose_name=_(TXT["page.original_language"]),
        help_text=_(TXT["page.original_language.help"]),
    )

    temporary_redirect = models.CharField(
        max_length=250,
        blank=True,
        default="",
        verbose_name=_(TXT["page.temporary_redirect"]),
        help_text=_(TXT["page.temporary_redirect.help"]),
    )

    is_creatable = False

    search_fields = Page.search_fields + [
        index.SearchField("title_de", partial_match=True, boost=2),
        index.SearchField("title_cs", partial_match=True, boost=2),
        index.FilterField("title_de"),
        index.FilterField("title_cs"),
    ]

    english_panels = [FieldPanel("title", classname="full title")]
    german_panels = [FieldPanel("title_de", classname="full title")]
    czech_panels = [FieldPanel("title_cs", classname="full title")]
    promote_panels = Page.promote_panels + [FieldPanel("temporary_redirect")]
    meta_panels = [
        FieldPanel("owner"),
        FieldPanel("editor"),
        FieldPanel("original_language"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(english_panels, heading=_(TXT["heading.en"])),
            ObjectList(german_panels, heading=_(TXT["heading.de"])),
            ObjectList(czech_panels, heading=_(TXT["heading.cs"])),
            ObjectList(promote_panels, heading=_(TXT["heading.promote"])),
            ObjectList(meta_panels, heading=_(TXT["heading.meta"])),
        ]
    )

    @cached_property
    def is_restricted(self):
        """Return True if this page is restricted to the public in any way."""
        return (
            self.get_view_restrictions()
            .exclude(restriction_type=BaseViewRestriction.NONE)
            .exists()
        )

    def serve(self, request, *args, **kwargs):
        """Return a redirect of the temporary_redirect property is set."""
        if self.temporary_redirect:
            return redirect(self.temporary_redirect, permanent=False)
        return super(I18nPage, self).serve(request, *args, **kwargs)

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
        changed=True,
    ):
        """Add applications and translation specific fields to the revision of the page."""

        # TODO: Add explicit read-only permission to support access to admin backend
        if user.groups.filter(name='READONLY').exists():
            raise PermissionDenied

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
        update_fields.append("latest_revision_created_at")

        self.draft_title = self.title
        self.draft_title_de = self.title_de
        self.draft_title_cs = self.title_cs
        update_fields.append("draft_title")
        update_fields.append("draft_title_de")
        update_fields.append("draft_title_cs")

        if changed:
            self.has_unpublished_changes = True
            update_fields.append("has_unpublished_changes")

        if update_fields:
            self.save(update_fields=update_fields)

        # Log
        LOGGER.info(
            f'Page edited: "{self.title}" id={self.pk} revision_id={revision.id}'
        )

        if submitted_for_moderation:
            LOGGER.info(
                f""""
            Page submitted for moderation: \"{self.title}\" id={self.pk} revision_id={revision.id}
            """
            )

        return revision

    def __str__(self):
        return str(self.i18n_title)


class CategoryPage(I18nPage):
    """
    A simple category page with a multilingual title fieldself.

    CategoryPages are simple pages that can only be created once at the root level of the CMS.
    """

    # class properties
    template = "cms/categories/category_page.html"

    @classmethod
    def can_create_at(cls, parent):
        """Make sure the page can only be created once in the page hierarchy."""
        return (
            super(CategoryPage, cls).can_create_at(parent) and not cls.objects.exists()
        )

    def get_context(self, request, *args, **kwargs):
        """Add child pages into the pages context."""
        context = super(CategoryPage, self).get_context(request, *args, **kwargs)
        child_pages = self.get_children().specific().live()
        context["child_pages"] = sorted(child_pages, key=lambda x: str(x.i18n_title))
        return context

    class Meta:
        abstract = True


class BlogPage(I18nPage):
    """A page of static content."""

    BLOG_EDITOR_FEATURES = [
        "h3",
        "h4",
        "h5",
        "h6",
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

    parent_page_types = ["HomePage", "BlogPage"]
    template = "cms/blog_page.html"

    body = StreamField(
        block_types=[
            ("heading", CharBlock(classname="full title")),
            ("paragraph", RichTextBlock(features=BLOG_EDITOR_FEATURES)),
            ("image", ImageChooserBlock()),
        ],
        blank=True,
        default=[],
    )
    body_de = StreamField(
        block_types=[
            ("heading", CharBlock(classname="full title")),
            ("paragraph", RichTextBlock(features=BLOG_EDITOR_FEATURES)),
            ("image", ImageChooserBlock()),
        ],
        blank=True,
        default=[],
    )
    body_cs = StreamField(
        block_types=[
            ("heading", CharBlock(classname="full title")),
            ("paragraph", RichTextBlock(features=BLOG_EDITOR_FEATURES)),
            ("image", ImageChooserBlock()),
        ],
        blank=True,
        default=[],
    )
    i18n_body = TranslatedField.named("body", True)

    english_panels = I18nPage.english_panels + [StreamFieldPanel("body")]
    german_panels = I18nPage.german_panels + [StreamFieldPanel("body_de")]
    czech_panels = I18nPage.czech_panels + [StreamFieldPanel("body_cs")]

    edit_handler = TabbedInterface(
        [
            ObjectList(english_panels, heading=_(TXT["heading.en"])),
            ObjectList(german_panels, heading=_(TXT["heading.de"])),
            ObjectList(czech_panels, heading=_(TXT["heading.cs"])),
            ObjectList(I18nPage.promote_panels, heading=_(TXT["heading.promote"])),
            ObjectList(I18nPage.meta_panels, heading=_(TXT["heading.meta"])),
        ]
    )

    class Meta:
        db_table = DB_TABLE_PREFIX + "_content_pages"
        verbose_name = _(TXT["blog"])
        verbose_name_plural = _(TXT["blog.plural"])


class HomePage(BlogPage):
    """The root page of the LIS cms site."""

    parent_page_types = ["wagtailcore.Page"]
    template = "cms/blog_page.html"

    class Meta:
        db_table = DB_TABLE_PREFIX + "homepage"
        verbose_name = _(TXT["home"])
        verbose_name_plural = _(TXT["home.plural"])
