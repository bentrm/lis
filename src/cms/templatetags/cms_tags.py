from django import template
from django.utils.translation import gettext
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


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def humanize_list(arg):
    print(arg)
    output = ""
    if len(arg) == 1:
        return str(arg[0])
    elif len(arg) > 1:
        output += ", ".join((str(x) for x in arg[:-1]))
        output += f" {gettext('and')} {arg[-1]}"
    return output
