import base64

from django.conf import settings
from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    """Поле для получения картинки в кодировке Base64."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            file_extension = format.split("/")[-1]
            data = ContentFile(
                base64.b64decode(imgstr), name="recipe." + file_extension
            )
        return super().to_internal_value(data)

    def to_representation(self, value):
        if not value:
            return None
        try:
            url = value.url
        except AttributeError:
            return None
        request = self.context.get("request")
        if not request:
            return None
        return "".join([request.scheme, "://", settings.SITE_DOMAIN, url])
