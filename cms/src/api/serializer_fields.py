from html.parser import HTMLParser

from rest_framework import serializers
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.views.serve import generate_image_url


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


class RenditionField(serializers.Field):
    def __init__(self, operation='fill-100x100|jpegquality-40', **kwargs):
        super().__init__(**kwargs)
        self.operation = operation

    def to_representation(self, value):
        """
        Serialize the value's class name.
        """
        if value:
            return generate_image_url(value, self.operation)


class TranslationField(serializers.Field):
    def get_attribute(self, instance):
        return instance

    def to_representation(self, instance):
        field = instance._meta.get_field(self.source)
        getter = 'i18n_' + self.source
        value = getattr(instance, getter)

        if isinstance(field, RichTextField):
            if TextExtractor.extract_text(value):
                return value
            else:
                return ''
        elif isinstance(field, StreamField):
            return value.stream_data if value else []
        else:
            return value
