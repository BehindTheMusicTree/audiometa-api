# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial **AudioMeta API** service: metadata session upload and session-download endpoints, docs, and tests split out from HearTheMusicTree API.
- **`POST /v1/audio/metadata/full/`** — read full file metadata (same behaviour as previously on HearTheMusicTree API); documentation in `docs/api/audio_metadata.md`.
