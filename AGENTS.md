# Project guidance

AudioMeta API is a Django/DRF service for audio metadata and short-lived
metadata sessions. Read `README.md` for the API and setup, and `CONTRIBUTING.md`
for project conventions. The default local setup uses SQLite, local memory cache
and on-disk session files; external fingerprinting is optional.

Existing project conventions are documented in `.cursorrules` and
`.cursor/rules/`; consult the relevant rules and verify them against the actual
repository configuration before applying them. The shared startup skill is in
`.agents/skills/launch/SKILL.md`, linked from `.claude/skills/launch`.
