from django.db import models
from wagtail.search.index import FilterField


class PointField(FilterField):
    def get_value(self, obj):
        try:
            field = self.get_field(obj.__class__)
            value = field.value_from_object(obj)
            return value.wkt
        except models.fields.FieldDoesNotExist:
            value = getattr(obj, self.field_name, None)
            if hasattr(value, "__call__"):
                value = value()
            return value
