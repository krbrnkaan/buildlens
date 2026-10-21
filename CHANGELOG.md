# Changelog

## 0.1.0 — 2026-10-22

First official GitHub release. No PyPI publication.

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

Official actions use reviewed full-SHA Node.js 24 pins and read-only token
permissions. Pre-release hosted validation passed on Ubuntu/Windows × Python
3.11–3.14; the GitHub Release records the exact final commit and its CI run.
macOS and Ubuntu 26 remain unverified. GitHub Private Vulnerability Reporting
is enabled, with independent non-maintainer access confirmed by the maintainer.
See SECURITY.md for confidential disclosure and best-effort redaction limits.
