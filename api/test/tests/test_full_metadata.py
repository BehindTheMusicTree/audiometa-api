from pathlib import Path
from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.serializer.audio_metadata.AudioMetadataFull import AudioMetadataFullSerializer
from api.serializer.audio_metadata.Fields import Fields
from api.utils.audio_fingerprinter import service as audio_fingerprinter_service
from api.utils.musicbrainz_recording_analysis import (
    ANALYSIS_CODE,
    ANALYSIS_ERROR,
    ANALYSIS_MESSAGE,
    ERROR_NO_MATCH,
)

pytestmark = pytest.mark.django_db

TEST_FILES = Path(__file__).resolve().parent.parent / "files"
MUSICBRAINZ_RAW_DATA_CAMEL = "musicbrainzRawData"


def _post_full_metadata(client, filename: str = "default.mp3", **kwargs):
    file_abs_path = TEST_FILES / filename
    with open(file_abs_path, "rb") as sample_file:
        data = {Fields.FILE: sample_file, **kwargs}
        return client.post(path=reverse("audio-metadata-full"), data=data, format="multipart")


def _force_include_musicbrainz_analysis_in_validated_data(serializer_class):
    original_is_valid = serializer_class.is_valid

    def patched_is_valid(self, raise_exception=False):
        result = original_is_valid(self, raise_exception=raise_exception)
        if hasattr(self, "_validated_data") and self._validated_data is not None:
            self._validated_data = dict(self._validated_data)
            self._validated_data[Fields.INCLUDE_MUSICBRAINZ_ANALYSIS] = True
        return result

    return patched_is_valid


@pytest.fixture
def client():
    return APIClient()


class TestFullMetadata:
    def test_post_default_mp3_then_200(self, client):
        response = _post_full_metadata(client)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None

    def test_include_musicbrainz_analysis_false_then_no_musicbrainz_raw_data(self, client):
        response = _post_full_metadata(client, **{Fields.INCLUDE_MUSICBRAINZ_ANALYSIS: False})
        assert response.status_code == status.HTTP_200_OK
        assert MUSICBRAINZ_RAW_DATA_CAMEL not in response.json()

    def test_include_musicbrainz_analysis_omitted_then_no_musicbrainz_raw_data(self, client):
        response = _post_full_metadata(client)
        assert response.status_code == status.HTTP_200_OK
        assert MUSICBRAINZ_RAW_DATA_CAMEL not in response.json()


class TestFullMetadataMusicbrainzMocks:
    def test_include_true_and_mb_match_then_raw_data_has_recording(self, client):
        mock_recording = {
            "id": "e2e-mock-recording-id",
            "title": "Mock Recording",
            "duration": 120,
            "score": 0.95,
            "artists": [{"id": "artist-1", "name": "Mock Artist"}],
        }
        with (
            patch.object(
                AudioMetadataFullSerializer,
                "is_valid",
                _force_include_musicbrainz_analysis_in_validated_data(AudioMetadataFullSerializer),
            ),
            patch(
                "api.view.AudioMetadataView.audio_fingerprinter_service.get_fingerprint_and_duration_for_analysis"
            ) as mock_fp,
            patch("api.view.AudioMetadataView.get_musicbrainz_recording_analysis") as mock_mb,
        ):
            mock_fp.return_value = {
                audio_fingerprinter_service.RESULT_FINGERPRINT: b"\x00" * 20,
                audio_fingerprinter_service.RESULT_DURATION_IN_SEC: 120.0,
                audio_fingerprinter_service.RESULT_ERROR_CODE: None,
                audio_fingerprinter_service.RESULT_ERROR_MESSAGE: None,
            }
            mock_mb.return_value = mock_recording
            response = _post_full_metadata(client)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert MUSICBRAINZ_RAW_DATA_CAMEL in data
        raw = data[MUSICBRAINZ_RAW_DATA_CAMEL]
        assert raw["id"] == mock_recording["id"]
        assert raw["title"] == mock_recording["title"]
        assert raw["artists"] == mock_recording["artists"]
        assert raw["score"] == mock_recording["score"]

    def test_include_true_and_mb_no_match_then_raw_data_has_error(self, client):
        error_payload = {
            ANALYSIS_ERROR: ERROR_NO_MATCH,
            ANALYSIS_CODE: ERROR_NO_MATCH,
            ANALYSIS_MESSAGE: "No matching recording found.",
        }
        with (
            patch.object(
                AudioMetadataFullSerializer,
                "is_valid",
                _force_include_musicbrainz_analysis_in_validated_data(AudioMetadataFullSerializer),
            ),
            patch(
                "api.view.AudioMetadataView.audio_fingerprinter_service.get_fingerprint_and_duration_for_analysis"
            ) as mock_fp,
            patch("api.view.AudioMetadataView.get_musicbrainz_recording_analysis") as mock_mb,
        ):
            mock_fp.return_value = {
                audio_fingerprinter_service.RESULT_FINGERPRINT: b"\x00" * 20,
                audio_fingerprinter_service.RESULT_DURATION_IN_SEC: 120.0,
                audio_fingerprinter_service.RESULT_ERROR_CODE: None,
                audio_fingerprinter_service.RESULT_ERROR_MESSAGE: None,
            }
            mock_mb.return_value = error_payload
            response = _post_full_metadata(client)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert MUSICBRAINZ_RAW_DATA_CAMEL in data
        raw = data[MUSICBRAINZ_RAW_DATA_CAMEL]
        assert raw["error"] == ERROR_NO_MATCH
        assert "code" in raw
        assert "message" in raw

    def test_include_true_and_fingerprint_fails_then_raw_data_has_error(self, client):
        with (
            patch.object(
                AudioMetadataFullSerializer,
                "is_valid",
                _force_include_musicbrainz_analysis_in_validated_data(AudioMetadataFullSerializer),
            ),
            patch(
                "api.view.AudioMetadataView.audio_fingerprinter_service.get_fingerprint_and_duration_for_analysis"
            ) as mock_fp,
        ):
            mock_fp.return_value = {
                audio_fingerprinter_service.RESULT_FINGERPRINT: None,
                audio_fingerprinter_service.RESULT_DURATION_IN_SEC: None,
                audio_fingerprinter_service.RESULT_ERROR_CODE: "timeout_error",
                audio_fingerprinter_service.RESULT_ERROR_MESSAGE: "Fingerprint request timed out.",
            }
            response = _post_full_metadata(client)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert MUSICBRAINZ_RAW_DATA_CAMEL in data
        raw = data[MUSICBRAINZ_RAW_DATA_CAMEL]
        assert raw["error"] == "fingerprint_failed"
        assert raw["code"] == "timeout_error"
        assert raw["message"] == "Fingerprint request timed out."
