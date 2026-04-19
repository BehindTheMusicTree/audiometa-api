import acoustid
from acoustid import WebServiceError

from api import settings
import api.exception.musicbrainz as musicbrainz_exception


class ApiFields:
    class Names:
        RESULTS = "results"
        RECORDINGS = "recordings"
        ID = "id"
        SCORE = "score"
        ARTISTS = "artists"
        NAME = "name"
        TITLE = "title"
        DATE = "date"
        DURATION_IN_SEC = "duration"
        RELEASEGROUPS = "releasegroups"
        RELEASES = "releases"
        DAY = "day"
        MONTH = "month"
        YEAR = "year"
        ERROR = "error"
        STATUS = "status"
        CODE = "code"
        MESSAGE = "message"

    class Values:
        class Status:
            OK = "ok"
            ERROR = "error"


class LookupMetaFields:
    RECORDINGS = "recordings"
    RELEASE_GROUPS = "releasegroups"
    RELEASES = "releases"
    COMPRESS = "compress"
    TRACKS = "tracks"


def get_best_recording_dict_with_score(recordings_grouped_by_score, duration_in_sec):
    def rate_groupe_of_recordings_by_score(group_of_recordings):
        return group_of_recordings[ApiFields.Names.SCORE]

    def rate_recording_by_similar_duration_and_by_number_of_fields(recording: dict):
        duration_fake = 1000000000
        duration_difference = abs(
            recording.get(ApiFields.Names.DURATION_IN_SEC, duration_fake) - duration_in_sec
        )
        fields_count = len(recording)
        release_groups_count = len(recording.get(ApiFields.Names.RELEASEGROUPS, []))
        return duration_difference, -fields_count, -release_groups_count

    best_group_of_recordings = max(recordings_grouped_by_score, key=rate_groupe_of_recordings_by_score)
    best_recordings = best_group_of_recordings[ApiFields.Names.RECORDINGS]
    best_recording = min(
        (recording for recording in best_recordings), key=rate_recording_by_similar_duration_and_by_number_of_fields
    )
    best_recording[ApiFields.Names.SCORE] = best_group_of_recordings[ApiFields.Names.SCORE]
    return best_recording


def _get_musicbrainz_best_recording_dict_from_fingerprint_and_duration(
    fingerprint: bytes, duration_in_sec: float
) -> dict | None:
    try:
        lookup = acoustid.lookup(
            apikey=settings.ACOUSTID_API_KEY,
            fingerprint=fingerprint,
            duration=duration_in_sec,
            meta=[
                LookupMetaFields.RECORDINGS,
                LookupMetaFields.RELEASE_GROUPS,
                LookupMetaFields.RELEASES,
                LookupMetaFields.COMPRESS,
                LookupMetaFields.TRACKS,
            ],
        )
        lookup_status = lookup[ApiFields.Names.STATUS]
        if lookup_status == ApiFields.Values.Status.OK:
            recordings_grouped_by_score = lookup[ApiFields.Names.RESULTS]
            if len(recordings_grouped_by_score) > 0:
                return get_best_recording_dict_with_score(
                    recordings_grouped_by_score=recordings_grouped_by_score, duration_in_sec=duration_in_sec
                )
            return None
        if lookup_status == ApiFields.Values.Status.ERROR:
            error_dict = lookup[ApiFields.Names.ERROR]
            error_code = error_dict[ApiFields.Names.CODE]
            error_message = error_dict[ApiFields.Names.MESSAGE]
            if error_code == 3:
                raise musicbrainz_exception.InvalidFingerprintMusicbrainzRecordingLookupException(
                    f'Musicbrainz original lookup error message: "{error_message}"'
                )
            if error_code == 5:
                raise musicbrainz_exception.InternalErrorMusicbrainzRecordingLookupException(
                    f'Musicbrainz original lookup error message: "{error_message}"'
                )
            exception_message = f"Error while getting MusicBrainz recording ID: {error_code} - {error_message}"
            raise musicbrainz_exception.UnknownErrorCodeMusicbrainzRecordingLookupException(exception_message)
        raise musicbrainz_exception.UnknownStatusMusicbrainzRecordingLookupException(lookup_status)
    except Exception as exception:
        if isinstance(exception, musicbrainz_exception.MusicbrainzRecordingLookupException):
            raise exception
        if isinstance(exception, WebServiceError):
            try:
                exc_str = str(exception)
            except Exception:
                exc_str = f"{type(exception).__name__}: <unable to stringify exception>"
            raise musicbrainz_exception.DNSResolutionErrorMusicbrainzRecordingLookupException(exc_str)
        try:
            exc_str = str(exception)
        except Exception:
            exc_str = f"{type(exception).__name__}: <unable to stringify exception>"
        raise musicbrainz_exception.UnknownErrorCodeMusicbrainzRecordingLookupException(exc_str)


ANALYSIS_ERROR = "error"
ANALYSIS_CODE = "code"
ANALYSIS_MESSAGE = "message"

ERROR_DURATION_TOO_SHORT = "duration_below_or_equal_1_sec"
ERROR_NO_API_KEY = "no_acoustid_api_key"
ERROR_NO_MATCH = "no_match"
ERROR_INVALID_FINGERPRINT = "invalid_fingerprint"
ERROR_INTERNAL = "internal_error"
ERROR_UNKNOWN_RESPONSE_CODE = "unknown_response_error_code"
ERROR_UNKNOWN_STATUS = "unknown_response_status_code"
ERROR_DNS = "dns_resolution_error"
ERROR_UNKNOWN = "unknown_error"

_EXCEPTION_TO_ERROR_CODE = {
    musicbrainz_exception.InvalidFingerprintMusicbrainzRecordingLookupException: ERROR_INVALID_FINGERPRINT,
    musicbrainz_exception.InternalErrorMusicbrainzRecordingLookupException: ERROR_INTERNAL,
    musicbrainz_exception.UnknownErrorCodeMusicbrainzRecordingLookupException: ERROR_UNKNOWN_RESPONSE_CODE,
    musicbrainz_exception.UnknownStatusMusicbrainzRecordingLookupException: ERROR_UNKNOWN_STATUS,
    musicbrainz_exception.DNSResolutionErrorMusicbrainzRecordingLookupException: ERROR_DNS,
}


def get_musicbrainz_recording_analysis(fingerprint: bytes, duration_in_sec: float) -> dict:
    if duration_in_sec <= 1:
        return {
            ANALYSIS_ERROR: ERROR_DURATION_TOO_SHORT,
            ANALYSIS_CODE: ERROR_DURATION_TOO_SHORT,
            ANALYSIS_MESSAGE: "Duration must be greater than 1 second for AcoustID lookup.",
        }
    if not (getattr(settings, "ACOUSTID_API_KEY", None) or "").strip():
        return {
            ANALYSIS_ERROR: ERROR_NO_API_KEY,
            ANALYSIS_CODE: ERROR_NO_API_KEY,
            ANALYSIS_MESSAGE: "AcoustID API key not configured.",
        }
    try:
        recording_dict = _get_musicbrainz_best_recording_dict_from_fingerprint_and_duration(
            fingerprint=fingerprint, duration_in_sec=duration_in_sec
        )
        if not recording_dict:
            return {
                ANALYSIS_ERROR: ERROR_NO_MATCH,
                ANALYSIS_CODE: ERROR_NO_MATCH,
                ANALYSIS_MESSAGE: "No matching recording found.",
            }
        return recording_dict
    except musicbrainz_exception.MusicbrainzRecordingLookupException as e:
        code = _EXCEPTION_TO_ERROR_CODE.get(type(e), ERROR_UNKNOWN)
        return {
            ANALYSIS_ERROR: code,
            ANALYSIS_CODE: code,
            ANALYSIS_MESSAGE: str(e),
        }
