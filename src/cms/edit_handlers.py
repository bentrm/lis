import uuid

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, widget_with_script


class FieldPanelTabs(MultiFieldPanel):
    """A panel that groups fields and multifields in a number of tabs."""

    template = "cms/edit_handlers/field_panel_tabs.html"
    js_template = "cms/edit_handlers/field_panel_tabs.js"

    def __init__(self, *args, **kwargs):
        self.id = uuid.uuid4()
        self.show_label = kwargs.pop("show_label", True)
        super().__init__(*args, **kwargs)

    def clone(self):
        return self.__class__(
            children=self.children,
            heading=self.heading,
            show_label=self.show_label,
            classname=self.classname,
            help_text=self.help_text,
        )

    def classes(self):
        classes = super().classes()
        classes.append("tabbed-field")
        return classes

    def id_for_label(self):
        return self.id

    def render(self):
        formset = render_to_string(
            self.template, {"self": self, "show_label": self.show_label}
        )
        js = self.render_js_init()
        return widget_with_script(formset, js)

    def render_js_init(self):
        return mark_safe(render_to_string(self.js_template, {"self": self}))


class FieldPanelTab(FieldPanel):
    def on_instance_bound(self):
        self.bound_field = self.form[self.field_name]
        self.heading = self.heading if self.heading else self.bound_field.label
        self.help_text = self.bound_field.help_text

    @property
    def required(self):
        return self.bound_field.field.required

    def render_as_field(self):
        return mark_safe(
            render_to_string(
                self.field_template,
                {
                    "field": self.bound_field,
                    "show_label": False,
                    "field_type": self.field_type(),
                },
            )
        )
