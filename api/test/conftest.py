import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

from api import settings


@pytest.fixture(autouse=True)
def mock_acoustid_lookup(request):
    if request.node.get_closest_marker("real_acoustid"):
        yield
        return
    with patch(
        "api.utils.musicbrainz_recording_analysis.acoustid.lookup",
        return_value={"status": "ok", "results": []},
    ):
        yield


@pytest.fixture(autouse=True)
def mock_audio_fingerprinter(request):
    if request.node.get_closest_marker("real_fingerprinter"):
        yield
        return
    with patch(
        "api.utils.audio_fingerprinter.utils.post_fingerprint_audio",
        return_value=(b"\x00" * 32, 120.0),
    ):
        yield


@pytest.fixture(autouse=True)
def cleanup_metadata_session_dir():
    yield
    session_dir = getattr(settings, "METADATA_SESSION_DIR", None)
    if session_dir and Path(session_dir).is_dir():
        for entry in Path(session_dir).iterdir():
            if entry.is_file():
                try:
                    entry.unlink()
                except OSError:
                    pass


@pytest.fixture(autouse=True)
def use_tmp_session_dir(tmp_path, monkeypatch):
    d = tmp_path / "metadata-sessions"
    d.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(settings, "METADATA_SESSION_DIR", d)
