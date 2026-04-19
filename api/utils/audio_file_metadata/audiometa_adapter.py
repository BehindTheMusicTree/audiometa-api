import os
from typing import Any

import audiometa
from audiometa.exceptions import FileCorruptedError as AudiometaFileCorruptedError
from django.core.files import File as DjangoFile
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models.fields.files import FieldFile

from api.utils.audio_file_metadata.exceptions import FileCorruptedError
from api.utils.file_path_utils import get_file_path as _get_file_path_util

FILE_TYPE = TemporaryUploadedFile | FieldFile | str | DjangoFile


def update_file_metadata_unified(
    file: FILE_TYPE,
    unified_metadata: dict[str, Any],
    normalized_rating_max_value: int | None = None,
) -> None:
    file_path = _get_file_path_util(file)
    audiometa.update_metadata(
        file=file_path,
        unified_metadata=unified_metadata,
        normalized_rating_max_value=normalized_rating_max_value,
        warn_on_unsupported_field=False,
    )


def get_full_metadata(file: FILE_TYPE, include_raw_binary_data: bool) -> dict:
    file_path = _get_file_path_util(file)
    try:
        return audiometa.get_full_metadata(file=file_path, include_raw_binary_data=include_raw_binary_data)
    except AudiometaFileCorruptedError as e:
        raise FileCorruptedError(str(e)) from e
