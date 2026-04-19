from rest_framework import serializers


class AudioMetadataRequestUrlSerializer(serializers.Serializer):
    file = serializers.URLField(required=True)
    include_musicbrainz_analysis = serializers.BooleanField(required=False, default=False)
