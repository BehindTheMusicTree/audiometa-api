---
name: launch
description: Use this skill when asked to run, start, dev-serve, or preview audiometa-api, or to confirm a change works against the real service.
---

# Launch audiometa-api

Small Django service (metadata session upload/read/download). No user
accounts, no companion service required for the default local setup —
SQLite + Django's local memory cache + on-disk temp files under
`./metadata-sessions/`.

## 1. Install deps (first run, or after a dependency change)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install ".[dev]"
```

## 2. Set required env var

```bash
export DJANGO_SECRET_KEY=dev-secret
```

## 3. Migrate and start

```bash
python manage.py migrate --run-syncdb
python manage.py runserver
```

Default: `http://127.0.0.1:8000/`. Health check: `GET /health/`. API docs:
`GET /docs/` (Swagger UI), `GET /schema/` (OpenAPI).

## Optional integrations

- `ACOUSTID_API_KEY` — enables AcoustID lookups.
- `AFP_BASE_URL`, `AFP_PORT`, `AFP_POST_ENDPOINT` — point at a running
  Audio Fingerprinter service to enable `include_musicbrainz_analysis` /
  fingerprinting on session upload. Not required for basic metadata
  read/write.

## Verify

```bash
pytest
```
