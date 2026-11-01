# Contributing to AudioMeta API

Thanks for helping improve this service. The repo follows the same engineering habits as [HearTheMusicTree API](https://github.com/BehindTheMusicTree/hear-the-music-tree-api); many conventions are encoded in **agent rules** under `.claude/rules/` (loaded natively by Claude Code) (see below).

## Agent rules (read when editing)

These mirror the parent API repo except **private-resource filtering** (not applicable here—no per-user library models).

| Rule                                                                                           | Purpose                                       |
| ---------------------------------------------------------------------------------------------- | --------------------------------------------- |
| [one-class-per-file.md](.claude/rules/one-class-per-file.md)                                 | One class per file                            |
| [divide-test-cases.md](.claude/rules/divide-test-cases.md)                                   | Split test cases                              |
| [use-assert-not-assertequal.md](.claude/rules/use-assert-not-assertequal.md)                 | Prefer `assert` over `assertEqual`            |
| [field-name-constants.md](.claude/rules/field-name-constants.md)                             | Field name constants                          |
| [pull-request-convention.md](.claude/rules/pull-request-convention.md)                       | PR conventions                                |
| [openapi-validation-documentation.md](.claude/rules/openapi-validation-documentation.md)     | OpenAPI / validation docs                     |
| [pre-pr-checklist.md](.claude/rules/pre-pr-checklist.md)                                     | Pre-PR checklist                              |
| [issue-description-in-separate-file.md](.claude/rules/issue-description-in-separate-file.md) | Issue drafts location                         |
| [changelog-best-practices.md](.claude/rules/changelog-best-practices.md)                     | Changelog style                               |
| [changelog-entry-placement.md](.claude/rules/changelog-entry-placement.md)                   | Where to add changelog entries                |
| [test-naming-convention.md](.claude/rules/test-naming-convention.md)                         | Test naming                                   |
| [use-custome-validation-exception.md](.claude/rules/use-custome-validation-exception.md)     | Custom validation errors                      |
| [no-useless-comments.md](.claude/rules/no-useless-comments.md)                               | Avoid noise comments                          |
| [use-pipe-none.md](.claude/rules/use-pipe-none.md)                                           | Prefer `\|` for optional types                |
| [issue-template-usage.md](.claude/rules/issue-template-usage.md)                             | Issue templates                               |
| [pr-description-in-separate-file.md](.claude/rules/pr-description-in-separate-file.md)       | PR descriptions in `.github/pr-descriptions/` |
| [commit-message-convention.md](.claude/rules/commit-message-convention.md)                   | Commit messages                               |
| [test-structure.md](.claude/rules/test-structure.md)                                         | Test layout                                   |
| [git-flow-workflow.md](.claude/rules/git-flow-workflow.md)                                   | Git Flow / branches                           |

Pinned dependencies and draft doc locations: [dependency-pinning.md](.claude/rules/dependency-pinning.md).

## Prerequisites

- **Python** 3.12+ (3.14 is fine if available)
- **Git**

Docker is **not** required for the default test suite (SQLite + locmem cache). Optional: Docker or a local [Audio Fingerprinter](https://github.com/BehindTheMusicTree/audio-fingerprinter) + `ACOUSTID_API_KEY` if you work on `include_musicbrainz_analysis` against real services.

## Local setup

```bash
git clone https://github.com/BehindTheMusicTree/audiometa-api.git
cd audiometa-api

python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install ".[dev]"

# Optional: copy env template and adjust
cp env/dev/.env.dev.example env/.env
# load_dotenv() in settings reads from cwd; you can export vars instead

export DJANGO_SECRET_KEY=dev-not-for-production
pytest
```

Run the app:

```bash
export DJANGO_SECRET_KEY=dev-not-for-production
python manage.py migrate --run-syncdb
python manage.py runserver
```

Open `http://127.0.0.1:8001/docs/` for Swagger.

## Tests

```bash
pytest
```

Tests live under `api/test/tests/`. Pytest options are in **`pyproject.toml`** under `[tool.pytest.ini_options]` (no separate `pytest.ini`). Conftest mocks external AcoustID/fingerprint calls by default so CI stays offline-friendly.

## Changelog

Update `CHANGELOG.md` under **`[Unreleased]`** for user-visible changes (see [changelog-best-practices.md](.claude/rules/changelog-best-practices.md)).

## Pull requests

- Use **Git Flow**-style branch names where possible (`feature/...`, `chore/...`); see [git-flow-workflow.md](.claude/rules/git-flow-workflow.md) and the parent repo if your team enforces branch protection the same way.
- Draft longer PR bodies under `.github/pr-descriptions/` per [pr-description-in-separate-file.md](.claude/rules/pr-description-in-separate-file.md).
- Run through [pre-pr-checklist.md](.claude/rules/pre-pr-checklist.md) before requesting review.

## CI

GitHub Actions runs `pytest` on pull requests to `main` / `develop` (see `.github/workflows/test.yml`).

## License

See [LICENSE](LICENSE).
