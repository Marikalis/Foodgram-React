import base64

from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64StrToFile(serializers.ImageField):
    def to_internal_value(self, data):
        fmt, imgstr = data.split(';base64,')
        ext = fmt.split('/')[-1]
        return ContentFile(base64.b64decode(imgstr), name='img.' + ext)
