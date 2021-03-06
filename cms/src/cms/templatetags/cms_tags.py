from html.parser import HTMLParser

from django import template
from django.urls import reverse
from django.utils.translation import gettext
from wagtail.core.templatetags.wagtailcore_tags import pageurl

register = template.Library()


@register.simple_tag
def get_verbose_name(object):
    return object._meta.verbose_name


@register.simple_tag(name="cmsurl", takes_context=True)
def cms_url(context, page):
    """Return the given pages url or the current pages draft url if in preview mode."""
    request = context["request"]

    if not page:
        return None
    if hasattr(request, "is_preview") and request.is_preview:
        return reverse("wagtailadmin_pages:view_draft", args=(page.id,))
    return pageurl(context, page)


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def humanize_list(arg):
    output = ""
    if len(arg) == 1:
        return str(arg[0])
    elif len(arg) > 1:
        output += ", ".join((str(x) for x in arg[:-1]))
        output += f" {gettext('and')} {arg[-1]}"
    return output


class TextExtractor(HTMLParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = ""

    def handle_data(self, data):
        self.text += data

    @classmethod
    def extract_text(cls, data):
        self = cls()
        self.feed(data)
        self.close()
        return self.text

    def error(self, message):
        pass


@register.filter
def dehtmlize(value):
    return TextExtractor.extract_text(value)
