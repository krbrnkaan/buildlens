# Milestone 1.5 — independent MVP hardening

> Historical checkpoint, not current compatibility or remote status. The private
> repository now exists and all eight initial hosted jobs passed in run 39667229407.
> See [milestone 2B](milestone-2b-report.md) for current changes and release gates.

Date: 2026-10-21. Scope: the actual BuildLens implementation in this workspace,
not just the previous report. No other local project was inspected or reused.

Historical checkpoint. [Milestone 1.6](milestone-1.6-report.md) supersedes its
compatibility and publication status. Reproduction paths below were normalized
for public documentation; historical test results remain unchanged.

**Verdict: READY for publication as an early, explicitly limited open-source MVP;
NOT READY for an unqualified cross-platform production-release claim.** Python
3.11 and hosted/native Ubuntu CI remain UNVERIFIED. No repository was published,
pushed, or given a remote. Work stops at local verification.

## Findings, ranked by severity

All implementation fixes below are complete. Unverified environment checks are
listed separately rather than presented as passing tests.

### High — must fix before sharing reports

1. **Common secret values could escape masking.** In `redaction.py`, a password
   containing an escaped quote left its trailing characters visible. CLI-style
   `--password value`, npm `_auth`, non-Basic/Bearer Authorization headers, and
   database URL credentials also escaped the existing patterns. Synthetic
   reproducers exposed these values in reports and argument-error output.
   **Fixed:** escaped quoted values, secret arguments, `_auth`, full authorization
   header values, and scheme-based URL userinfo are masked. Tests cover terminal,
   JSON, Markdown, query tokens, JWT-shaped tokens, Slack-shaped tokens, and AWS
   secret-key assignments. Each secret-bearing fixture is confirmed present in
   report evidence so omission caps cannot create a false passing test. Markdown
   escaping is removed before checking for leaked substrings.

2. **Permitted text could make redaction impractically slow.** The URL pattern
   retried many possible username/password divisions in long colon-heavy text;
   scheme-like and JWT-like text also caused repeated overlapping scans. A
   single permitted 16 KiB URL-like line took approximately 1.9 seconds. A
   repeated synthetic input timed out after 10 seconds before the fix.
   **Fixed:** remove the redundant URL division and prevent overlapping starts
   inside scheme/token-shaped identifiers. The regression test passed in the
   recorded 0.69-second pytest run after the fix, then passed in every platform
   suite. No general runtime or memory ceiling is promised.

### Medium — correctness and safe failure handling

3. **Specific diagnoses could be displayed without decisive evidence.** A long
   `npm error ... ERESOLVE` line was categorized correctly but its excerpt cut
   off the actual `ERESOLVE` code. **Fixed:** the excerpt window retains the match
   tail within the existing 1,000-character cap. Excerpts remain contiguous pieces
   of the sanitized original line, apart from the documented `... ` marker.

4. **Patterns confused unrelated failures and missed common variants.** A
   compiler's `invalid token in expression` was classified as authentication;
   tool-agnostic `No matching version found` as npm; two-part `name:value` text as
   a JVM dependency. An invalid access token and missing `action.yaml` were
   missed. **Fixed:** require authentication-specific token wording, npm context,
   or three-part Gradle coordinates where appropriate; recognize both action
   metadata extensions. `ImportError: cannot import name` remains UNKNOWN, with
   honest generic evidence, rather than being called a missing module.

5. **Output write failures broke the exit-code contract.** A closed pipe on
   Windows produced an uncaught OSError and exit 1; buffered writes could also
   fail at interpreter shutdown. **Fixed:** flush inside the protected write,
   handle OSError, suppress repeated shutdown flushing, and return 2 for failed
   report writes. Tests cover both normal and JSON input-error reports. Syntax
   errors still use argparse's stderr usage output rather than JSON.

6. **A regular-file check preceded a potentially blocking open.** A path replaced
   by a FIFO after `stat()` could block before the descriptor-type check. This
   follows from the actual code order; a real-FIFO reproducer is UNVERIFIED on
   this workspace filesystem. **Mitigated:** open with POSIX nonblocking flags
   where available, then check the opened descriptor and close rejected inputs.
   The descriptor/cleanup regression passes under WSL. A real FIFO subprocess
   regression is included for native POSIX CI, with a timeout, but skipped here
   because the Windows-backed filesystem rejects FIFO creation.

7. **Formatted reader exceptions retained raw OS exception details.** The CLI
   already caught InputError, but a caller formatting the chained traceback could
   expose an OS error containing sensitive text. **Fixed:** suppress the OS cause
   in normal traceback presentation; keep a fixed, useful input error message.
   Exception objects still exist in memory. This is not secure memory erasure.

8. **Bidirectional controls could visually spoof terminal evidence.** A Unicode
   right-to-left override survived sanitization. **Fixed:** remove bidi override
   and isolate controls while preserving original physical line numbering.

### Low — verification and release-process gaps

9. **Packaging/CI checks were too narrow.** The old smoke check covered only one
   console invocation, and the matrix omitted Python 3.12/3.13. JSON fields were
   documented but had no machine-readable schema artifact or field-shape
   regression. **Improved:** an installed-wheel smoke script checks source-import
   isolation, all formats, UNKNOWN, input errors, help, and version; a JSON Schema
   and contract tests protect field shapes and a known fingerprint. The manifest
   includes schema, tools, samples, and CI configuration. No runtime dependency
   was added. Ubuntu/Windows × Python 3.11/3.12/3.13/3.14 is now configured.

## Architecture assessment and changes

No architectural rewrite was warranted. Bounded decoding → redaction → rules →
grouping → report model → rendering remains intact. The renderer consumes
sanitized report data. Runtime code has no network client or log-derived command
execution. Group ordering, report models, input limits, CLI syntax, version
0.1.0, and JSON schema version 1.0 remain unchanged. More conservative redaction
can change fingerprints for newly masked inputs; the fingerprint algorithm itself
is unchanged.

Modified:

- `src/buildlens/redaction.py`, `reader.py`, `rules.py`, `analyzer.py`, `cli.py`.
- `tests/test_buildlens.py` (read-error regression now targets the native open).
- `.github/workflows/ci.yml`, `.gitignore`, `MANIFEST.in`.
- `README.md`, `SECURITY.md`, `docs/json-schema.md`, `docs/milestone-report.md`.

Added:

- `tests/test_hardening.py` — adversarial security, detection, evidence, resource,
  CLI, descriptor, and contract cases.
- `samples/adversarial.log` — synthetic unrelated failures, duplicate errors,
  fake instructions, and invalid credential-shaped strings.
- `docs/report.schema.json` — machine-readable success/input-error shapes.
- `tools/smoke_wheel.py` — standard-library installed-wheel assertions.
- This milestone report.

No runtime dependencies or major features were added. No commits, remotes,
publication, deployment, global software installation, LLM calls, API keys,
telemetry, paid services, or private logs were used. Development package downloads
were used to prepare project-local virtual environments; analysis itself is offline.

## Actual test and compatibility results

The baseline was rerun before editing: **63 passed** on Windows/Python 3.14.
The first adversarial run reproduced **11 failures, 12 passes, 1 skip**. Those
failures were fixed; additional regression cases were then added. The final suite
contains **93 collected cases**, including meaningful parameterized signatures
and output formats, not 93 different functions.

| Environment | Full suite | Wheel installation / isolated imports | Console CLI |
| --- | --- | --- | --- |
| Windows, Python 3.12.10 | **91 passed, 2 skipped** | PASS | PASS |
| Windows, Python 3.13.13 | **91 passed, 2 skipped** | PASS | PASS |
| Windows, Python 3.14.0 | **91 passed, 2 skipped** | PASS, separate clean runtime venv | PASS |
| Ubuntu under WSL, Python 3.12.3 | **92 passed, 1 skipped** | PASS, project-local venv | PASS |
| Python 3.11, either platform | **UNVERIFIED — unavailable** | UNVERIFIED | UNVERIFIED |
| Native/hosted Ubuntu matrix | **UNVERIFIED — CI not run** | UNVERIFIED | UNVERIFIED |

Windows skips are the POSIX FIFO and nonblocking-descriptor regressions. WSL
passes the descriptor test but skips real FIFO creation with `Operation not
supported`. Ubuntu 22.04 was also available with Python 3.10.12, below the
declared minimum; it was not counted as a supported-environment pass. Docker was
unavailable. No system packages were installed to change these results.

Other executed checks:

- Ruff lint and format checking: **PASS on Windows and WSL Linux**.
- Wheel and source archive build: **PASS**.
- Wheel installation with `--no-index --no-deps`: **PASS** on all four tested
  runtime environments. The Windows 3.14 smoke environment has no test tooling.
- `tools/smoke_wheel.py`: **PASS** on all four environments. Module launches use
  `-I`, remove PYTHONPATH, run from a temporary directory inside this workspace,
  and reject imports from `src/`. Console entry points were checked separately.
- `pip check`: **PASS** on all four wheel environments.
- JSON from the installed console commands parsed successfully and produced
  the expected six diagnosis groups for the mixed sample.

No coverage percentage, external audit, native Linux release certification, or
hosted CI pass is claimed. Synthetic tests cover Gradle/Maven, npm, Python,
GitHub Actions, generic/unknown failures, unrelated errors, duplicates, ANSI,
Unicode, invalid bytes, near-limit input, embedded fake instructions, and common
secret formats. Evidence is compared with the sanitized original at its actual
line number; fabricated line 999 from the fake instruction never becomes evidence.

## Reproduce locally

Windows development setup and checks:

```powershell
# Start in the BuildLens repository root.
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest -q -rs
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m build
py -3.12 -m venv .venv-wheel
.\.venv-wheel\Scripts\python.exe -m pip install --no-index --no-deps dist/buildlens-0.1.0-py3-none-any.whl
.\.venv-wheel\Scripts\python.exe tools/smoke_wheel.py
.\.venv-wheel\Scripts\buildlens.exe analyze samples/adversarial.log --format json
```

On Linux use a Python 3.11+ interpreter and the environment's `bin/python` and
`bin/buildlens`. README contains setup, actual example output, limitations,
privacy warnings, and troubleshooting. For simultaneous version tests use
distinct `--basetemp` and pytest `cache_dir` paths; the audit did so.

## Remaining risks and publication verdict

- Redaction remains best effort. Malformed or split credentials, cookie values,
  unfamiliar token formats, sensitive paths, usernames, and proprietary text can
  remain. Review reports before sharing. Original logs are unchanged and still
  contain original secrets.
- Rules identify symptoms, not proven causes. Quoted errors can match; localized
  or multiline-only signatures can be missed. Masking can remove useful context.
  UNKNOWN does not indicate success. Output limits intentionally omit evidence.
- Inputs must be stable local files. The descriptor check does not make hostile
  filesystems or concurrent regular-file mutation safe, and real-FIFO behavior
  has not executed on this workspace's filesystem.
- Python 3.11 and the hosted/native platform matrix still need actual execution.
  WSL verification is evidence for that environment, not a native CI substitute.
- Before claiming a broadly verified release, run the configured matrix and
  establish the maintainer's public/private security reporting channel.

**GitHub publication: CONDITIONAL READY as an early MVP with these limitations
visible. A fully verified production release is NOT READY.** Publishing remains
a separate user decision; this task performed no publication or push.

Skipped: additional features and system-level environment installation.
Unverified: Python 3.11, hosted/native Ubuntu CI, and a real FIFO on this filesystem.
