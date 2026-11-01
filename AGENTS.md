# Project guidance

AudioMeta API is a Django/DRF service for audio metadata and short-lived
metadata sessions. Read `README.md` for the API and setup, and `CONTRIBUTING.md`
for project conventions. The default local setup uses SQLite, local memory cache
and on-disk session files; external fingerprinting is optional.

Before relevant work, read the shared project rules below. Paths are relative to the
repository root; `**/` includes root files. Also consult rules for associated
activities such as commits and PRs, even when no file is edited.

- For `**/*`, read `.agents/rules/changelog-best-practices.md`.
- For `**/*`, read `.agents/rules/changelog-entry-placement.md`.
- For `**/*`, read `.agents/rules/commit-message-convention.md`.
- For `**/*`, read `.agents/rules/dependency-pinning.md`.
- For `**/*`, read `.agents/rules/divide-test-cases.md`.
- For `**/*`, read `.agents/rules/field-name-constants.md`.
- For `**/*`, read `.agents/rules/git-flow-workflow.md`.
- For `**/*`, read `.agents/rules/issue-description-in-separate-file.md`.
- For `**/*`, read `.agents/rules/issue-template-usage.md`.
- For `**/*`, read `.agents/rules/no-useless-comments.md`.
- For `**/*`, read `.agents/rules/one-class-per-file.md`.
- For `api/view/**/*.py`, read `.agents/rules/openapi-validation-documentation.md`.
- For `**/*`, read `.agents/rules/pr-description-in-separate-file.md`.
- For `**/*`, read `.agents/rules/pre-pr-checklist.md`.
- For `**/*`, read `.agents/rules/pull-request-convention.md`.
- For `**/*`, read `.agents/rules/test-naming-convention.md`.
- For `**/*`, read `.agents/rules/test-structure.md`.
- For `**/*`, read `.agents/rules/use-assert-not-assertequal.md`.
- For `**/*`, read `.agents/rules/use-custome-validation-exception.md`.
- For `**/*.py`, read `.agents/rules/use-pipe-none.md`.

Edit shared rules and regenerate Claude adapters using [agent-config v1.1.0](https://github.com/BehindTheMusicTree/agent-config): `python3 /path/to/agent-config/scripts/render-project-rules.py . --apply`. The startup skill is shared at `.agents/skills/launch/SKILL.md`. Graphify is optional when installed.
