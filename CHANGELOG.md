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
without assigning an unverified cause. Known limitation: quoted example errors
can be mistaken for actual symptoms. See SECURITY.md and the milestone 1.6 report.
