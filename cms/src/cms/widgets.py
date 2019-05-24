import json

from django import forms
from django.contrib.gis.geos import Point
from django.utils import six
from mapwidgets.widgets import BasePointFieldMapWidget, minify_if_not_debug
from mapwidgets.settings import mw_settings


class CustomGooglePointFieldWidget(BasePointFieldMapWidget):
    template_name = "mapwidgets/google-point-field-widget.html"
    settings = mw_settings.GooglePointFieldWidget
    settings_namespace = "GooglePointFieldWidget"
    google_map_srid = 4326

    @property
    def media(self):
        css = {
            "all": [
                minify_if_not_debug("mapwidgets/css/map_widgets{}.css"),
            ]
        }

        js = [
            "https://maps.googleapis.com/maps/api/js?libraries=places&language={}&key={}".format(
                mw_settings.LANGUAGE, mw_settings.GOOGLE_MAP_API_KEY
            )
        ]

        if not mw_settings.MINIFED:  # pragma: no cover
            js = js + [
                "mapwidgets/js/jquery_class.js",
                "mapwidgets/js/django_mw_base.js",
                "mapwidgets/js/mw_google_point_field.js",
            ]
        else:
            js = js + [
                "mapwidgets/js/mw_google_point_field.min.js"
            ]

        return forms.Media(js=js, css=css)

    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = dict()

        field_value = {}
        if value and isinstance(value, six.string_types):
            value = self.deserialize(value)
            longitude, latitude = value.coords
            field_value["lng"] = longitude
            field_value["lat"] = latitude

        if isinstance(value,  Point):
            if value.srid and value.srid != self.google_map_srid:
                ogr = value.ogr
                ogr.transform(self.google_map_srid)
                value = ogr

            longitude, latitude = value.coords
            field_value["lng"] = longitude
            field_value["lat"] = latitude

        extra_attrs = {
            "options": self.map_options(),
            "field_value": json.dumps(field_value)
        }
        attrs.update(extra_attrs)
        self.as_super = super(CustomGooglePointFieldWidget, self)
        if renderer is not None:
            return self.as_super.render(name, value, attrs, renderer)
        else:
            return self.as_super.render(name, value, attrs)
