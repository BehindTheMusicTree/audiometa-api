from typing import Any

from django.core.exceptions import ImproperlyConfigured
from rest_framework.exceptions import ValidationError as DrfValidationError

from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode


class AppValidationException(DrfValidationError):
    DEFAULT_FIELD = "unhandled"

    status_code = 400
    error_type = "app_validation_error"
    message: str
    field_validation_error_code: FieldValidationErrorCode

    def __init__(
        self,
        message: str,
        field_validation_error_code: FieldValidationErrorCode,
        field_name: str | None = DEFAULT_FIELD,
    ):
        self.field = field_name if field_name else self.DEFAULT_FIELD
        self.message = message
        self.field_validation_error_code = field_validation_error_code
        error_detail = {
            "message": message,
            "code": field_validation_error_code,
            "field": self.field,
            "error_type": self.error_type,
        }
        self.errors = {self.field: error_detail}
        super().__init__(self.errors)

    @classmethod
    def _detect_and_convert_from_drf_exception(cls, exc: DrfValidationError) -> "AppValidationException | None":
        if not isinstance(exc, DrfValidationError) or not hasattr(exc, "detail"):
            return None
        try:
            detail = exc.detail
        except (AttributeError, TypeError):
            return None
        if isinstance(detail, list):
            detail = {"error": detail[0] if detail else "Unknown error"}
        if not isinstance(detail, dict):
            return None

        def has_error_type(error_dict: dict[str, Any]) -> bool:
            if not isinstance(error_dict, dict):
                return False
            if error_dict.get("error_type") == cls.error_type:
                return True
            return any(
                has_error_type(value) for value in error_dict.values() if isinstance(value, dict)
            )

        if has_error_type(detail):
            return cls.from_drf_validation_error(detail)
        return None

    @classmethod
    def from_drf_validation_error(cls, detail: dict[str, Any]) -> "AppValidationException":
        if not isinstance(detail, dict):
            raise ImproperlyConfigured("Detail must be a dictionary")

        def extract_error_details(error_dict: dict[str, Any], parent_field: str = "") -> tuple | None:
            if all(key in error_dict for key in ("message", "code")):
                field = error_dict.get("field", parent_field)
                return (field, str(error_dict["message"]), str(error_dict["code"]))
            for field, field_detail in error_dict.items():
                if isinstance(field_detail, dict):
                    result = extract_error_details(field_detail, field)
                    if result:
                        return result
            return None

        error_details = extract_error_details(detail)
        if error_details:
            field, message, code = error_details
            try:
                fvec = FieldValidationErrorCode(code)
            except ValueError:
                fvec = FieldValidationErrorCode.DEFAULT
            return cls(field_name=field, message=message, field_validation_error_code=fvec)
        return cls(
            message=str(detail),
            field_validation_error_code=FieldValidationErrorCode.FORMAT_INVALID,
            field_name=cls.DEFAULT_FIELD,
        )
