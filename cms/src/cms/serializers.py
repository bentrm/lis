import base64
import hashlib
import hmac
from html.parser import HTMLParser

from django.conf import settings
from django.urls import reverse
from django.utils.encoding import force_text
from rest_framework import serializers
from wagtail.core.fields import RichTextField, StreamField

from cms.models import ImageMedia


def generate_signature(image_id, filter_spec, key=None):
    if key is None:
        key = settings.SECRET_KEY

    # Key must be a bytes object
    if isinstance(key, str):
        key = key.encode()

    # Based on libthumbor hmac generation
    # https://github.com/thumbor/libthumbor/blob/b19dc58cf84787e08c8e397ab322e86268bb4345/libthumbor/crypto.py#L50
    url = '{}/{}/'.format(image_id, filter_spec)
    return force_text(base64.urlsafe_b64encode(hmac.new(key, url.encode(), hashlib.sha1).digest()))


def verify_signature(signature, image_id, filter_spec, key=None):
    return force_text(signature) == generate_signature(image_id, filter_spec, key=key)


def generate_image_url(image, filter_spec, viewname='wagtailimages_serve', key=None):
    signature = generate_signature(image.id, filter_spec, key)
    url = reverse(viewname, args=(signature, image.id, filter_spec))
    url += image.file.name[len('original_images/'):]
    return url


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
            # TODO: Translate
            return field.stream_block.get_api_representation(value, self.context)
            # return value.stream_data if value else []
        else:
            return value


class RenditionField(serializers.Field):
    def __init__(self, operation='fill-100x100|jpegquality-40', source='self', **kwargs):
        super().__init__(source, **kwargs)
        self.operation = operation

    def get_attribute(self, instance):
        return instance

    def to_representation(self, instance):
        """
        Serialize the value's class name.
        """
        value = getattr(instance, self.source) if self.source == 'self' else instance

        if value:
            return generate_image_url(value, self.operation)


class ImageSerializer(serializers.ModelSerializer):
    title = TranslationField()
    caption = TranslationField()
    copyright = serializers.CharField()
    thumb = RenditionField(operation='fill-250x250|jpegquality-60')
    banner = RenditionField(operation='fill-800x400|jpegquality-60')
    small = RenditionField(operation='max-250x250|jpegquality-60')
    mid = RenditionField(operation='max-500x500|jpegquality-60')
    large = RenditionField(operation='max-800x800|jpegquality-60')

    class Meta:
        model = ImageMedia
        fields = (
            'id',
            'title',
            'caption',
            'copyright',
            'thumb',
            'banner',
            'small',
            'mid',
            'large',
        )
