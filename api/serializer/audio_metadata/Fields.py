from enum import StrEnum

from audiometa import UnifiedMetadataKey

from api.serializer.audio_metadata.AudioMetadataRequestFieldKey import AudioMetadataRequestFieldKey


class Fields(StrEnum):
    FILE = AudioMetadataRequestFieldKey.FILE.value
    INCLUDE_MUSICBRAINZ_ANALYSIS = AudioMetadataRequestFieldKey.INCLUDE_MUSICBRAINZ_ANALYSIS.value
    SESSION_TOKEN = AudioMetadataRequestFieldKey.SESSION_TOKEN.value
    SESSION_EXPIRES_IN_SECONDS = AudioMetadataRequestFieldKey.SESSION_EXPIRES_IN_SECONDS.value
    TITLE = "title"
    ARTISTS = UnifiedMetadataKey.ARTISTS.value
    ALBUM = UnifiedMetadataKey.ALBUM.value
    ALBUM_ARTISTS = UnifiedMetadataKey.ALBUM_ARTISTS.value
    GENRES_NAMES = "genres_names"
    RATING = "rating"
    LANGUAGE = "language"
