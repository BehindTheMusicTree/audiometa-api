from enum import Enum


class FieldValidationErrorCode(str, Enum):
    DEFAULT = "validation_error"
    FORMAT_INVALID = "format_invalid"
    REQUIRED = "required"
    BLANK = "blank"
    FILE_TOO_LARGE = "file_too_large"
    FILE_TOO_SMALL = "file_too_small"
    TRACK_FILE_TYPE_INVALID = "track_file_type_invalid"
    TRACK_FILE_EXTENSION_INVALID = "track_file_extension_invalid"
    URL_INVALID = "url_invalid"
    URL_NOT_FOUND = "url_not_found"
    URL_REQUEST_FAILED = "url_request_failed"
    TRACK_FILE_DOWNLOAD_FAILED = "track_file_download_failed"
    STRING_TOO_LONG = "string_too_long"
    STRING_TOO_SHORT = "string_too_short"
    RATING_TOO_SMALL = "rating_too_small"
    RATING_TOO_LARGE = "rating_too_large"

    def __str__(self) -> str:
        return str(self.value)
