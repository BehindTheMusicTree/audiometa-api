from rest_framework import serializers


class AudioMetadataRequestFileSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
    include_musicbrainz_analysis = serializers.BooleanField(required=False, default=False)
