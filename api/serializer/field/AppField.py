from typing import Any

from rest_framework.fields import Field, ListField

from api.exception.validation.app.AppValidationException import AppValidationException
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode


class AppField(Field):
    validation_error_code_mapping: dict[str, FieldValidationErrorCode] = {
        "required": FieldValidationErrorCode.REQUIRED,
        "null": FieldValidationErrorCode.REQUIRED,
        "blank": FieldValidationErrorCode.BLANK,
        "invalid": FieldValidationErrorCode.FORMAT_INVALID,
        "invalid_extension": FieldValidationErrorCode.TRACK_FILE_EXTENSION_INVALID,
        "invalid_choice": FieldValidationErrorCode.FORMAT_INVALID,
        "does_not_exist": FieldValidationErrorCode.FORMAT_INVALID,
        "incorrect_type": FieldValidationErrorCode.FORMAT_INVALID,
        "max_length": FieldValidationErrorCode.STRING_TOO_LONG,
        "min_length": FieldValidationErrorCode.STRING_TOO_SHORT,
        "max_value": FieldValidationErrorCode.RATING_TOO_LARGE,
        "min_value": FieldValidationErrorCode.RATING_TOO_SMALL,
        "max_size": FieldValidationErrorCode.FILE_TOO_LARGE,
        "min_size": FieldValidationErrorCode.FILE_TOO_SMALL,
    }

    invalid_message_validation_error_code_mapping: dict[str, FieldValidationErrorCode] = {
        "Not a valid string.": FieldValidationErrorCode.FORMAT_INVALID,
        "Invalid UUID format.": FieldValidationErrorCode.FORMAT_INVALID,
    }

    def fail(self, key: str, **kwargs: Any) -> None:
        try:
            msg = self.error_messages[key]
            if kwargs:
                msg = msg.format(**kwargs)
        except KeyError:
            class_name = self.__class__.__name__
            msg = f"Invalid input for {class_name}."

        if key == "invalid":
            if msg.startswith("Failed to download file:"):
                code = FieldValidationErrorCode.TRACK_FILE_DOWNLOAD_FAILED
            else:
                code = self.invalid_message_validation_error_code_mapping.get(
                    msg, FieldValidationErrorCode.DEFAULT
                )
        else:
            code = self.validation_error_code_mapping.get(key, FieldValidationErrorCode.DEFAULT)

        raise AppValidationException(
            field_name=self.get_error_field_name(), message=msg, field_validation_error_code=code
        )

    def get_error_field_name(self) -> str | None:
        if hasattr(self, "field_name") and self.field_name:
            field_name = self.field_name
            if getattr(self, "many", False) or isinstance(self, ListField):
                field_name += "[]"
            return field_name
        return None

    def to_internal_value(self, data: Any) -> Any:
        return None
