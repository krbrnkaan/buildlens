# BuildLens milestone 0–1 report

Historical baseline: statuses below describe that checkpoint only. The private
repository now exists and all eight initial hosted jobs passed in run 39667229407.
See [milestone 2B](milestone-2b-report.md) for current results and release gates.

Assessment: **READY for local MVP use and contributor review.** This is not a
claim of production certification or verified Linux/Python 3.11 runtime behavior.

## Delivered files

The workspace began empty. All of these files are new:

- Packaging: `pyproject.toml`, `MANIFEST.in`.
- CLI/package: `src/buildlens/__init__.py`, `src/buildlens/__main__.py`,
  `src/buildlens/cli.py`.
- Core: `src/buildlens/models.py`, `src/buildlens/reader.py`,
  `src/buildlens/redaction.py`, `src/buildlens/rules.py`,
  `src/buildlens/analyzer.py`, `src/buildlens/render.py`.
- Validation: `tests/test_buildlens.py`, `.github/workflows/ci.yml`.
- Synthetic examples: `samples/mixed.log`, `samples/lockfile.log`,
  `samples/permissions.log`, `samples/unknown.txt`.
- Documentation/governance: `README.md`, `LICENSE`, `CONTRIBUTING.md`,
  `SECURITY.md`, `AGENTS.md`, `.gitignore`, `docs/json-schema.md`, this report.

A local Git repository was initialized on `main`. No remote was configured and
no commit, push, publication, deployment, or global installation was performed.
Ignored local artifacts include `.venv`, `.venv-smoke`, test/build caches,
`dist/buildlens-0.1.0-py3-none-any.whl`, and `dist/buildlens-0.1.0.tar.gz`.

## Problem, users, and architecture

BuildLens helps developers and CI maintainers identify recognizable failure
symptoms from local logs without uploading sensitive material. It does not
verify root causes or determine whether an arbitrary build succeeded.

The small processing pipeline is: bounded regular-file read and decoding →
secret/control sanitization → explicit signature matching → stable fingerprint
grouping → shared report model → terminal, JSON, or Markdown rendering. The CLI
owns argument parsing and exit codes. Runtime dependencies: **none**.

## Functional capabilities

- `buildlens analyze <logfile>` and `python -m buildlens analyze <logfile>`.
- Terminal, `--format json`, and `--format markdown` output.
- Gradle/Maven dependency failures; npm resolution and lockfile errors; Python
  missing modules; permissions; exhausted storage; authentication failures;
  GitHub Actions action-resolution/metadata errors.
- Cautious explanations and recommended investigation steps, with evidence and
  original one-based line numbers. Generic exit messages do not override specific
  symptoms. Insufficient recognized evidence produces `UNKNOWN`.
- Duplicate grouping from rule ID and normalized, redacted message text.
- UTF-8/BOM and BOM-marked UTF-16, imperfect decoding warnings, LF/CRLF/CR,
  ANSI/control stripping, common secret redaction, and escaped Markdown/HTML.
- Versioned JSON contract (`1.0`) and documented exit codes: 0 supported diagnosis,
  1 UNKNOWN, 2 invalid input/usage. Exit 0 is not a successful-build indication.
- Limits: 10 MiB, 100,000 lines, 16,384 characters per line; 100 diagnosis groups,
  five evidence excerpts per group, 1,000 characters per excerpt.

## Exact installation and run commands

PowerShell, starting from the workspace:

```powershell
# Start in the BuildLens repository root.
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\buildlens.exe analyze samples/mixed.log
.\.venv\Scripts\buildlens.exe analyze samples/mixed.log --format json
.\.venv\Scripts\buildlens.exe analyze samples/mixed.log --format markdown
.\.venv\Scripts\python.exe -m buildlens analyze samples/unknown.txt
```

The last command intentionally exits 1. Initial installation requires locally
available tooling or package downloads; log analysis requires no network access.
README also includes Linux setup and offline wheel installation instructions.

## Validation evidence

Executed locally on Windows with Python **3.14.0**, pytest **9.1.1**, and Ruff
**0.17.1**:

| Check | Actual result |
| --- | --- |
| `python -m pytest -q --tb=short` | **63 passed**, no failed/skipped tests |
| `python -m ruff check . --output-format concise` | Passed |
| `python -m ruff format --check .` | Passed |
| `python -m build` | Wheel and source archive built successfully |
| Fresh `.venv-smoke` wheel install with `--no-index --no-deps` | Passed |
| Installed console script, all three formats, without source PYTHONPATH | Passed; JSON parsed and contained six groups on mixed sample |
| Installed `python -m buildlens` on unknown sample | Valid JSON, UNKNOWN, exit 1 |
| Clean installed environment `python -m pip check` | No broken requirements |
| Python 3.11 syntax parser check | All nine package modules accepted |
| Wheel source bytes compared with workspace | Matched |

Tests cover supported signatures, false positives and unknowns, specificity
precedence, original line numbers, duplicate counts and caps, secret redaction
across output formats, unchanged input bytes, invalid inputs, resource limits,
encoding/newlines, terminal escapes, Markdown injection, usage and exit codes,
synthetic samples, read permission failure, and non-execution of log commands.

Validation discovered and fixed SSH classification, npm false positives,
argument-error secret leakage, long-line evidence truncation, generic occurrence
counts, and multiline terminal-sequence line-number drift. A resource probe also
found slow secret matching: a 16 KiB neutral identifier exceeded a five-second
timeout before the fix and completed in approximately 0.002 seconds afterward.
The CLI regression test guards against this class of stall with a timeout.

No coverage percentage is claimed. Linux and Python 3.11 runtime checks were not
executed here; GitHub Actions is configured for Windows/Linux × Python 3.11/3.14
but has not run because there is no remote repository. Serena was unavailable.

## Limitations and security

Recognition is primarily English and line-oriented. Quoted examples of known
errors can match. Unknown tools, multiline-only signatures, localized messages,
and obfuscated errors may be missed. A report can describe several symptoms
without establishing their causal relationship. Grouping preserves package
names, paths, and versions, so messages differing in those fields remain separate.

Secret masking is best effort, not a guarantee that a report is safe to publish.
Paths, usernames, private text, unknown secret formats, and split/obfuscated
credentials may remain. Review reports before sharing and protect original logs.
The analyzer contains no network requests, subprocess execution, or automatic
remediation. It reads bounded files without modifying them. Analyze stable local
files rather than allowing untrusted users to replace paths during a read.

## Suggested next milestone

Improve precision with additional synthetic negative/overlap cases, add bounded
workflow-step context, and extend supported log formats while retaining the
offline deterministic architecture. Run the configured platform matrix before
making a broader compatibility claim.

**READY** for the requested local foundation and functional MVP.

Skipped: dashboards, cloud services, bots, LLMs, databases, automatic fixes, and
remote publishing. Remaining risks: rule errors and incomplete redaction; Linux
and Python 3.11 runtime compatibility remain unverified locally.
