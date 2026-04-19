# Contributing to AudioMeta API

Thanks for helping improve this service. The repo follows the same engineering habits as [HearTheMusicTree API](https://github.com/BehindTheMusicTree/hear-the-music-tree-api); many conventions are encoded in **Cursor rules** under `.cursor/rules/` (see below).

## Cursor rules (read when editing)

These mirror the parent API repo except **private-resource filtering** (not applicable here—no per-user library models).

| Rule                                                                                           | Purpose                                       |
| ---------------------------------------------------------------------------------------------- | --------------------------------------------- |
| [one-class-per-file.mdc](.cursor/rules/one-class-per-file.mdc)                                 | One class per file                            |
| [divide-test-cases.mdc](.cursor/rules/divide-test-cases.mdc)                                   | Split test cases                              |
| [use-assert-not-assertequal.mdc](.cursor/rules/use-assert-not-assertequal.mdc)                 | Prefer `assert` over `assertEqual`            |
| [field-name-constants.mdc](.cursor/rules/field-name-constants.mdc)                             | Field name constants                          |
| [pull-request-convention.mdc](.cursor/rules/pull-request-convention.mdc)                       | PR conventions                                |
| [focused-tests.mdc](.cursor/rules/focused-tests.mdc)                                           | Focused tests                                 |
| [openapi-validation-documentation.mdc](.cursor/rules/openapi-validation-documentation.mdc)     | OpenAPI / validation docs                     |
| [pre-pr-checklist.mdc](.cursor/rules/pre-pr-checklist.mdc)                                     | Pre-PR checklist                              |
| [issue-description-in-separate-file.mdc](.cursor/rules/issue-description-in-separate-file.mdc) | Issue drafts location                         |
| [changelog-best-practices.mdc](.cursor/rules/changelog-best-practices.mdc)                     | Changelog style                               |
| [changelog-entry-placement.mdc](.cursor/rules/changelog-entry-placement.mdc)                   | Where to add changelog entries                |
| [test-naming-convention.mdc](.cursor/rules/test-naming-convention.mdc)                         | Test naming                                   |
| [use-custome-validation-exception.mdc](.cursor/rules/use-custome-validation-exception.mdc)     | Custom validation errors                      |
| [no-useless-comments.mdc](.cursor/rules/no-useless-comments.mdc)                               | Avoid noise comments                          |
| [use-pipe-none.mdc](.cursor/rules/use-pipe-none.mdc)                                           | Prefer `\|` for optional types                |
| [issue-template-usage.mdc](.cursor/rules/issue-template-usage.mdc)                             | Issue templates                               |
| [comments.mdc](.cursor/rules/comments.mdc)                                                     | When to comment                               |
| [pr-description-in-separate-file.mdc](.cursor/rules/pr-description-in-separate-file.mdc)       | PR descriptions in `.github/pr-descriptions/` |
| [commit-message-convention.mdc](.cursor/rules/commit-message-convention.mdc)                   | Commit messages                               |
| [test-structure.mdc](.cursor/rules/test-structure.mdc)                                         | Test layout                                   |
| [git-flow-workflow.mdc](.cursor/rules/git-flow-workflow.mdc)                                   | Git Flow / branches                           |

Also see the repo root [`.cursorrules`](.cursorrules) (pinned dependencies, draft doc locations).

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

Update `CHANGELOG.md` under **`[Unreleased]`** for user-visible changes (see [changelog-best-practices.mdc](.cursor/rules/changelog-best-practices.mdc)).

## Pull requests

- Use **Git Flow**-style branch names where possible (`feature/...`, `chore/...`); see [git-flow-workflow.mdc](.cursor/rules/git-flow-workflow.mdc) and the parent repo if your team enforces branch protection the same way.
- Draft longer PR bodies under `.github/pr-descriptions/` per [pr-description-in-separate-file.mdc](.cursor/rules/pr-description-in-separate-file.mdc).
- Run through [pre-pr-checklist.mdc](.cursor/rules/pre-pr-checklist.mdc) before requesting review.

## CI

GitHub Actions runs `pytest` on pull requests to `main` / `develop` (see `.github/workflows/test.yml`).

## License

See [LICENSE](LICENSE).
