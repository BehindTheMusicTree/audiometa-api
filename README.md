# AudioMeta API

Small Django service for the **metadata session** flow: upload audio (or URL), read metadata, then download the file with tags written using a short-lived session token. No user accounts; sessions use Django cache and on-disk temp files.

## Endpoints

| Step | Method | Path |
|------|--------|------|
| Create session | `POST` | `/v1/audio/metadata/session/` |
| Download with tags | `POST` | `/v1/audio/metadata/session-download/` |
| Health | `GET` | `/health/` |
| OpenAPI schema | `GET` | `/schema/` |
| Swagger UI | `GET` | `/docs/` |

See [docs/api/audio_metadata_session.md](docs/api/audio_metadata_session.md) and [docs/frontend/one_time_metadata_update.md](docs/frontend/one_time_metadata_update.md).

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DJANGO_SECRET_KEY=dev-secret
pytest
```

For local run (defaults: SQLite, locmem cache, session dir under `./metadata-sessions/`):

```bash
export DJANGO_SECRET_KEY=dev-secret
python manage.py migrate --run-syncdb
python manage.py runserver
```

Optional: `ACOUSTID_API_KEY`, Audio Fingerprinter (`AFP_BASE_URL`, `AFP_PORT`, `AFP_POST_ENDPOINT`) for `include_musicbrainz_analysis` / fingerprinting on session upload.

## Related

- [audiometa-python](https://github.com/BehindTheMusicTree/audiometa) — metadata read/write library  
- [HearTheMusicTree API](https://github.com/BehindTheMusicTree/hear-the-music-tree-api) — main library API (still exposes `POST /v1/audio/metadata/full/` for read-only metadata)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

See [LICENSE](LICENSE).
