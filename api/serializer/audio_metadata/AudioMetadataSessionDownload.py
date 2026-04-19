from rest_framework import serializers

from api.serializer.audio_metadata.WritableMetadataFieldsMixin import WritableMetadataFieldsMixin


class AudioMetadataSessionDownloadSerializer(WritableMetadataFieldsMixin):
    session_token = serializers.CharField(required=False, allow_blank=False)
