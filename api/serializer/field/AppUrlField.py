from typing import Any

from rest_framework import serializers

from api.serializer.field.AppField import AppField


class AppUrlField(AppField, serializers.URLField):
    def to_internal_value(self, data: Any) -> str:
        return serializers.URLField.to_internal_value(self, data)
