from enum import Enum


class AudioMetadataRequestFieldKey(str, Enum):
    FILE = "file"
    INCLUDE_MUSICBRAINZ_ANALYSIS = "include_musicbrainz_analysis"
    SESSION_TOKEN = "session_token"
    SESSION_EXPIRES_IN_SECONDS = "session_expires_in_seconds"
