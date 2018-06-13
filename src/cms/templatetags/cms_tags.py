from django import template
from django.urls import reverse

from wagtail.core.templatetags.wagtailcore_tags import pageurl

register = template.Library()

@register.simple_tag(name="cmsurl", takes_context=True)
def cms_url(context, page):
    """Return the given pages url or the current pages draft url if in preview mode."""
    if not page:
        return None
    if context["request"].is_preview:
        return reverse("wagtailadmin_pages:view_draft", args=(page.id,))
    return pageurl(context, page)
