# BuildLens

Version 0.1.0 release preparation. No public repository release or package
publication is claimed. See the [draft release notes](docs/releases/v0.1.0.md).

BuildLens is an independent, offline command-line tool that turns a CI/build log
into a small report of recognizable failures, supporting evidence, and cautious
next steps. It is for developers and maintainers triaging failed builds locally,
including environments where logs cannot be uploaded to an external service.

It uses deterministic, reviewable rules. It has **no runtime dependencies, network
requests, telemetry, API keys, LLM calls, or automatic fixes**. It never executes
log contents and never changes the input file. A diagnosis identifies a reported
symptom, not a proven root cause. An unsupported or inconclusive log returns
`UNKNOWN`, including a successful log: BuildLens is not a build success detector.

## Install

Requires Python 3.11 or newer. From the project directory:

Windows PowerShell (use the Python launcher rather than an older `python`):

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\buildlens.exe analyze samples/mixed.log
.\.venv\Scripts\python.exe -m buildlens analyze samples/mixed.log --format json
```

Linux/macOS:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/buildlens analyze samples/mixed.log
.venv/bin/python -m buildlens analyze samples/mixed.log --format json
```

The initial development install downloads build/test tooling. Analysis itself
works offline. For runtime-only installation use `pip install .` inside a virtual
environment. An offline install requires a previously built wheel:
`python -m pip install --no-index --no-deps /path/to/buildlens-0.1.0-py3-none-any.whl`.

After activating the environment, the interface is:

```sh
buildlens analyze samples/mixed.log
buildlens analyze samples/mixed.log --format json
buildlens analyze samples/mixed.log --format markdown
python -m buildlens analyze samples/unknown.txt
```

Output goes to stdout; redirect it to save a report. Human-readable input errors
go to stderr. With `--format json`, input errors are JSON on stdout. Invalid CLI
syntax uses argparse's usage message on stderr, even when JSON was requested.

| Exit | Meaning |
| --- | --- |
| 0 | At least one supported diagnosis was found; this does **not** mean the build passed |
| 1 | Analysis completed with `UNKNOWN` |
| 2 | Input or command usage error, or a report output write failure |

## Supported evidence

| Category | Examples |
| --- | --- |
| JVM_DEPENDENCY | Gradle unresolved configurations/coordinates; Maven missing or untransferable artifacts |
| NPM_DEPENDENCY | ERESOLVE, ETARGET, E404, unresolved dependency tree |
| NPM_LOCKFILE | Clean-install lockfile prerequisites, missing lockfile entries, out-of-sync manifests |
| PYTHON_MODULE | ModuleNotFoundError or ImportError reporting `No module named` |
| PERMISSION | EACCES, EPERM, permission denied, Windows access denied |
| DISK_SPACE | ENOSPC, no space left, disk full |
| AUTHENTICATION | Authentication failed, invalid access/authentication token, E401/E403, HTTP rejection, SSH public-key denial |
| GITHUB_ACTIONS | Action resolution/download failures and missing action metadata |
| UNKNOWN | Generic GitHub Actions exit messages, unsupported errors, empty or inconclusive logs |

Specific signatures take priority over generic exit wrappers. The first matching
rule on a line wins: disk, authentication, permissions, Python, npm lockfile,
npm dependency, JVM dependency, GitHub Actions. Generic messages appear as
evidence only when no supported diagnosis is found. Reports can contain multiple
distinct diagnoses, ordered by first appearance. There is no causal ranking.

## Input and reporting limits

- Regular `.log`/`.txt` files only, case-insensitive extension; symlinks to regular
  files are allowed. Inputs are read at most 10 MiB + one sentinel byte.
- Files over 10 MiB, 100,000 physical lines, or 16,384 characters per line are
  rejected rather than silently partially analyzed.
- UTF-8 (optional BOM) and BOM-marked UTF-16 are supported. Invalid bytes become
  replacement characters with a warning; legacy encodings are not guessed.
- LF, CRLF, and CR line endings are normalized. Evidence uses original one-based
  physical line numbers. ANSI styling/hyperlinks and C0/C1 controls are stripped.
- At most 100 distinct diagnosis groups and five evidence excerpts per group.
  Evidence is capped at 1,000 characters per line, with a window around the
  matching signature and `... ` marking an omitted prefix. Group omissions are warned.
  For signatures spanning more than the excerpt limit, the excerpt retains the
  matching tail (for example, the npm error code); the original log holds full context.
- Fingerprint: first 16 hex characters of SHA-256 over `rule_id + "\n" + text`,
  after redaction, case folding, whitespace collapsing, and removal of a leading
  ISO-style datetime. Package names, paths, and versions remain significant.
  Identical sanitized messages group together; different secret values may group
  together. Fingerprints are identifiers, not security guarantees.

## JSON contract

See [docs/json-schema.md](docs/json-schema.md) for schema version `1.0`, including
field types, evidence semantics, error output, and compatibility rules.
The accompanying [JSON Schema](docs/report.schema.json) describes report and
input-error objects without restricting future category names.

## Development

Use the virtual environment's Python for these commands:

```sh
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
python -m build
```

CI is configured for Windows and Ubuntu with Python 3.11, 3.12, 3.13, and 3.14.
It builds the wheel, installs it, and tests all formats and exit statuses using
`python tools/smoke_wheel.py` with isolated Python imports. CI is configured
locally; it will run only after a future, separately authorized remote setup.
Tests and samples use synthetic data only.

Locally verified: Windows with Python 3.11, 3.12, 3.13, and 3.14; Ubuntu under WSL
with Python 3.12. Hosted GitHub Actions, Linux Python 3.11/3.13/3.14, macOS,
and other unlisted environments remain **UNVERIFIED**. Python below 3.11 is unsupported.
The WSL checkout's normal filesystem cannot create FIFOs; real FIFO and symlink
checks also run on a temporary native Linux filesystem mounted privately inside
the checkout. See [the release preparation report](docs/milestone-1.6-report.md)
for exact results, skips, and remaining publication gates.

## Example output

`buildlens analyze samples/unknown.txt` exits 1 and prints:

```text
BuildLens: unknown.txt
Lines: 2

UNKNOWN (unknown)
Fingerprint: 7f51b4fb44dbc727; occurrences: 1
Insufficient recognized evidence to explain this log. This does not establish success.
Next step: Inspect the failing step and preceding output; capture a more detailed log if needed.
- L2: ##[error]Process completed with exit code 42.
```

Adding `--format json` returns a single object with `schema_version: "1.0"`,
category `UNKNOWN`, and evidence `{"line": 2, "text": "##[error]Process completed with exit code 42."}`.
Adding `--format markdown` produces escaped Markdown headings and evidence lists.
`samples/adversarial.log` demonstrates unrelated errors, duplicates, fake
instructions, and synthetic credentials. Embedded instructions are data only.

## Reproducible diagnostic evaluation

`python tools/evaluate.py` evaluates the labelled synthetic cases in
`samples/evaluation.json`. [Recorded results](docs/diagnostic-evaluation.json)
include a deliberately ambiguous quoted-documentation example that is currently
misclassified as a disk-space symptom. This is a known precision limit, not a
general accuracy benchmark or evidence of adoption by real users.

The evaluator checks original evidence positions, UNKNOWN cases, duplicate and
unrelated errors, and the presence of advice. Advice remains an investigation
suggestion; the evaluator cannot prove root causes or measure real developer usefulness.

## Troubleshooting

- **Python too old:** use `py -3.12` (or another installed 3.11+ interpreter) on
  Windows, or check `python3 --version` on Linux. The plain Windows `python`
  command can point to a different installation from `py`.
- **Command not found:** activate the virtual environment or use its explicit
  Python path with `-m buildlens`. Keep pip and Python in the same environment.
- **Missing ensurepip on Linux:** obtain venv support through your approved
  system setup process, or use an existing approved virtual environment. BuildLens
  does not install system packages for you.
- **UNKNOWN:** inspect the original step and earlier output. Exit wrappers alone
  cannot establish a cause; a clean log can also be UNKNOWN. Import errors that
  say `cannot import name` are currently generic rather than missing-module diagnoses.
- **File rejected:** supply a regular `.log`/`.txt` file within the documented
  limits. Split a copy of an oversized log; reported line numbers refer to that
  copy. Do not replace the input while it is being analyzed.
- **Invalid encoding warning:** export a copy as UTF-8 for more reliable evidence.
- **Output write failure (2):** check the output destination, available storage,
  and downstream pipe consumer. A broken destination may prevent any error report
  from being delivered.
- **Before sharing:** review sanitized reports for unknown secret formats,
  private text, and identifying paths; redaction is not a publication guarantee.

## Architecture and limitations

`reader` bounds and decodes input; `redaction` sanitizes it before detection;
`rules` defines signatures and advice; `analyzer` collects and groups evidence;
`models` defines the report; `render` formats it; `cli` owns arguments and exit
codes. All runtime code is under `src/buildlens`.

Rules primarily recognize English, line-oriented messages. Quoted example errors
can match; multiline-only signatures, custom tools, locale-specific errors, and
obfuscated failures can be missed. No dependency graph, repository inspection,
network verification, or execution occurs. Recommendations require human review.
Redaction is best effort: review reports before sharing, as paths, usernames,
proprietary text, unknown token formats, and unusual credential formats may remain.
See [SECURITY.md](SECURITY.md).

The next milestone should improve rule precision using more synthetic regression
cases, preserve step context, and add explicit support for additional log formats
without introducing network services or automated remediation.

Licensed under the [MIT License](LICENSE).
