import os
from typing import Any
from urllib.parse import urlparse

import requests
from django.core.files.uploadedfile import UploadedFile, TemporaryUploadedFile

from api import settings
from api.exception.validation.app.AppValidationException import AppValidationException
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.serializer.field.AppField import AppField
from api.serializer.field.AppFileField import AppFileField
from api.serializer.field.AppUrlField import AppUrlField
from api.validator.TrackFileValidator import TrackFileValidator
from api.validator.TrackUrlValidator import TrackUrlValidator


class TrackFileField(AppField):
    def __init__(self, **kwargs):
        self._allow_null = kwargs.get("allow_null", True)
        super().__init__(**kwargs)
        self.url_field = AppUrlField(validators=[TrackUrlValidator()], allow_null=self._allow_null)
        self.file_field = AppFileField(validators=[TrackFileValidator()], allow_null=self._allow_null)

    def bind(self, field_name: str, parent: Any) -> None:
        super().bind(field_name, parent)
        if self.url_field:
            self.url_field.bind(field_name, parent)
        if self.file_field:
            self.file_field.bind(field_name, parent)

    def _download_file_from_url(self, url: str) -> TemporaryUploadedFile:
        try:
            response = requests.get(url, stream=True, timeout=30)
            filename = os.path.basename(urlparse(url).path)
            if not filename:
                filename = "downloaded_track"
            content_disposition = response.headers.get("Content-Disposition")
            if content_disposition and "filename=" in content_disposition:
                filename = content_disposition.split("filename=")[1].strip("\"'")
            if not os.path.splitext(filename)[1]:
                content_type = response.headers.get("Content-Type", "")
                if "mpeg" in content_type:
                    filename += ".mp3"
                elif ".wav" in content_type:
                    filename += ".wav"
                elif "flac" in content_type:
                    filename += ".flac"
                else:
                    raise AppValidationException(
                        field_name=self.get_error_field_name(),
                        message="Invalid file extension. Supported formats are: mp3, wav, flac",
                        field_validation_error_code=FieldValidationErrorCode.TRACK_FILE_EXTENSION_INVALID,
                    )
            content_length = response.headers.get("Content-Length")
            file_size = int(content_length) if content_length else 0
            temp_file = TemporaryUploadedFile(
                name=filename,
                content_type=response.headers.get("Content-Type", ""),
                size=file_size,
                charset=None,
            )
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    temp_file.write(chunk)
            temp_file.seek(0)
            return temp_file
        except requests.Timeout:
            raise AppValidationException(
                field_name=self.get_error_field_name(),
                message="URL request timed out. Please try again.",
                field_validation_error_code=FieldValidationErrorCode.URL_REQUEST_FAILED,
            )
        except requests.RequestException as e:
            raise AppValidationException(
                field_name=self.get_error_field_name(),
                message=f"Failed to download file: {str(e)} ",
                field_validation_error_code=FieldValidationErrorCode.TRACK_FILE_DOWNLOAD_FAILED,
            )
        except Exception as e:
            raise AppValidationException(
                field_name=self.get_error_field_name(),
                message=f"Unexpected error while downloading file: {str(e)} ",
                field_validation_error_code=FieldValidationErrorCode.TRACK_FILE_DOWNLOAD_FAILED,
            )

    def to_internal_value(self, data: Any) -> Any:
        if data in [None, ""]:
            if not self._allow_null:
                self.fail("null")
            return None
        if isinstance(data, str):
            validated_url = self.url_field.to_internal_value(data)
            try:
                self.url_field.run_validators(validated_url)
            except AppValidationException as e:
                raise AppValidationException(
                    field_name=self.get_error_field_name(),
                    message=e.message,
                    field_validation_error_code=e.field_validation_error_code,
                )
            downloaded_file = self._download_file_from_url(validated_url)
            try:
                self.file_field.run_validators(downloaded_file)
            except AppValidationException as e:
                raise AppValidationException(
                    field_name=self.get_error_field_name(),
                    message=e.message,
                    field_validation_error_code=e.field_validation_error_code,
                )
            return downloaded_file
        if isinstance(data, UploadedFile):
            validated_file = self.file_field.to_internal_value(data)
            try:
                self.file_field.run_validators(validated_file)
            except AppValidationException as e:
                raise AppValidationException(
                    field_name=self.get_error_field_name(),
                    message=e.message,
                    field_validation_error_code=e.field_validation_error_code,
                )
            if len(validated_file.name) > settings.UPLOADED_TRACK_FILENAME_LEN_MAX:
                validated_file.name = validated_file.name[-settings.UPLOADED_TRACK_FILENAME_LEN_MAX :]
            return validated_file
        self.fail("invalid", detail="Field must be either a valid audio file or URL.")

    def to_representation(self, value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, str):
            return value
        return value.url if value and hasattr(value, "url") else ""
