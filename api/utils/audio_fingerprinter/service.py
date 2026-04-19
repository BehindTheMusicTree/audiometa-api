from django.core.files.base import File as DjangoFile

from . import exception
from . import utils

USER_ID_PLACEHOLDER_FOR_ANALYSIS = "anonymous"

RESULT_FINGERPRINT = "fingerprint"
RESULT_DURATION_IN_SEC = "duration_in_sec"
RESULT_ERROR_CODE = "error_code"
RESULT_ERROR_MESSAGE = "error_message"

_EPHEMERAL_ERROR_MAPPING = {
    exception.WrongFileExtension: "wrong_file_extension",
    exception.WrongFileType: "wrong_file_type",
    exception.FileNotInPool: "file_not_in_pool",
    exception.BadRequestException: "unknown_bad_request",
    exception.InternalServerException: "internal_error",
    exception.TimeoutException: "timeout_error",
    exception.FpcalcStatusException: "fpcalc_error_with_status_2",
    exception.UnknownUnprocessableEntityException: "unknown_unprocessable_entity_error",
    exception.ServiceNotFoundException: "service_not_found",
    exception.ConnectionException: "unknown_connexion_error",
}


def get_fingerprint_and_duration_for_analysis(file, title: str = "") -> dict:
    from api.utils.file_path_utils import get_file_name_system

    filename = get_file_name_system(file)
    try:
        fingerprint, duration_in_sec = utils.post_fingerprint_audio(
            filename=filename, title=title, user_id=USER_ID_PLACEHOLDER_FOR_ANALYSIS
        )
        return {
            RESULT_FINGERPRINT: fingerprint,
            RESULT_DURATION_IN_SEC: float(duration_in_sec),
            RESULT_ERROR_CODE: None,
            RESULT_ERROR_MESSAGE: None,
        }
    except exception.AudioFingerprinterException as e:
        error_code = _EPHEMERAL_ERROR_MAPPING.get(type(e), "unknown")
        message = getattr(e, "message", str(e))
        return {
            RESULT_FINGERPRINT: None,
            RESULT_DURATION_IN_SEC: None,
            RESULT_ERROR_CODE: error_code,
            RESULT_ERROR_MESSAGE: message,
        }
