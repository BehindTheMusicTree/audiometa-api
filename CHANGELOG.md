# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Dev tooling**: Added a `launch` Claude Code skill (`.claude/skills/launch/`) documenting how
  to start the service locally.

### Changed

- **Dependencies**: Declared in **PEP 621** `pyproject.toml` (pinned runtime deps + `dev` extra for pytest). Removed `requirements.txt`; pytest config lives under `[tool.pytest.ini_options]`.

### Added

- Initial **AudioMeta API** service: metadata session upload and session-download endpoints, docs, and tests split out from HearTheMusicTree API.
- **`POST /v1/full/`** — read full file metadata (same behaviour as previously on HearTheMusicTree API); documentation in `docs/api/audio_metadata.md`.
