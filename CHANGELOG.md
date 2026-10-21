# Changelog

## 0.1.0 — Unreleased

First release candidate. No GitHub release or package publication has occurred.

- Offline CLI for `.log` and `.txt` build logs, with terminal, JSON, and Markdown reports.
- Explicit signatures for Gradle/Maven, npm, Python missing modules, permissions,
  storage, authentication, and GitHub Actions failures.
- Cautious explanations, source line evidence, stable duplicate grouping, and UNKNOWN fallback.
- Bounded input, imperfect encoding handling, terminal-control removal, and best-effort redaction.
- JSON schema 1.0 and a standard-library-only runtime supporting Python 3.11+.
- Synthetic regression tests, demonstration logs, and a labelled diagnostic evaluation.
- Release preparation verifies wheel/source archives and isolated wheel installation.

The release candidate also retains generic Python exception lines as evidence
without assigning an unverified cause. Explicit `Documentation example:` lines
now remain UNKNOWN evidence instead of creating actionable diagnoses; quotations
without this label can still match. All 22 labelled synthetic evaluation cases
agree on categories and evidence lines; this is not real-world accuracy.

The initial private commit passed all eight hosted Ubuntu/Windows × Python
3.11–3.14 jobs in run 39667229407. Local preflight updates the two official action
pins to Node.js 24 revisions; the modified source and workflow still require a
new hosted run. See SECURITY.md and docs/milestone-2b-report.md.
