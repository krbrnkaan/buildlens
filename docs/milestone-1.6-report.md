# Milestone 1.6 — public release preparation

> Historical checkpoint. The private repository and initial commit now exist;
> all eight initial hosted jobs passed in run 39667229407. The quoted-documentation
> case is fixed locally in [milestone 2B](milestone-2b-report.md). Statements below
> about absent remotes, unrun CI and the old false positive describe this earlier
> checkpoint only, not the current candidate.

Date: 2026-10-21. Candidate: **BuildLens v0.1.0**, JSON schema **1.0**.

**Verdict: NOT READY to publish yet. Local release preparation is complete.**
Actual hosted CI and a documented private security reporting channel remain
release gates. This task created no remote, commit, tag, push, deployment, GitHub
release, or package publication. The checklist deliberately leaves those actions
pending explicit maintainer approval.

## 1. Changes made

- Reviewed the actual runtime, tests, prior milestone findings, documentation,
  Git state, distribution configuration, and every publication candidate file.
- Obtained Python 3.11.16 inside the ignored workspace tooling directory using
  an existing uv executable with registry/global-bin installation disabled.
  Executed the full suite and clean-wheel checks on that interpreter.
- Verified real FIFOs, symlinks to FIFOs, FIFO replacement, nonregular descriptor
  rejection, and cleanup on native Linux tmpfs in a private mount namespace.
  The mount point and test files stayed inside the checkout and were removed
  with the namespace; no system package installation was required.
- Added release/path/size/version regressions and a reproducible synthetic
  diagnostic evaluation. It found a narrow evidence gap: an ambiguous Python
  ImportError returned UNKNOWN without retaining its actual error line. Added
  a failing regression, then extended only generic exception-line recognition.
  The category remains UNKNOWN; no root cause was invented.
- Added changelog, draft release notes, issue forms, a publication checklist,
  artifact validation, and a Linux special-file check helper. Kept version
  0.1.0 and the existing architecture/runtime dependencies unchanged.
- Removed machine-specific absolute checkout paths from historical reproduction
  commands, strengthened ignore rules, and prepared reviewed files for local
  Git tracking. No individual author identities were invented.

The maintainer explicitly confirmed control of the workspace's rights and intent
to release under MIT during this milestone. The existing MIT text and collective
project copyright notice were preserved. This is a human ownership confirmation,
not an independent legal/provenance audit or a claim about contributor count.

## 2. Files added or modified

Added:

- `.gitattributes` — portable text treatment and LF for shell helpers.
- `.github/ISSUE_TEMPLATE/bug_report.yml`, `feature_request.yml`, `config.yml`.
- `CHANGELOG.md` — accurate, unreleased 0.1.0 history.
- `docs/releases/v0.1.0.md`, `docs/release-checklist.md`, this report.
- `docs/diagnostic-evaluation.json` — actual reproducible case results.
- `samples/evaluation.json` — 22 labelled, synthetic cases; no private/public-log copying.
- `tests/test_release.py` — 12 release regression cases after parameterization.
- `tools/evaluate.py`, `tools/check_distribution.py`, `tools/check_linux_fifo.sh`.

Modified:

- `src/buildlens/rules.py` — retain generic named Python exceptions as UNKNOWN evidence.
- `tests/test_buildlens.py` — analyze only log/text sample files, excluding the new JSON corpus.
- `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `docs/json-schema.md`.
- `docs/milestone-report.md`, `docs/milestone-1.5-report.md` — portable historical
  reproduction commands and a link to current status; previous results remain historical.
- `.gitignore`, `MANIFEST.in`, `.github/workflows/ci.yml`.

The public candidate set is 44 text files. Local environments, Python downloads,
tool caches, test files, and distribution outputs are ignored. Existing package
models, CLI syntax, rendering, input limits, and fingerprint algorithm remain intact.

All 44 reviewed files are staged locally for an eventual initial commit. The
staged privacy scan found only the seven intentional synthetic locations listed
below; staged whitespace checks passed. Ignore checks excluded all eight sampled
local/secret paths. There is no remote or commit, and no ignored directory was staged.

## 3. Test results and skipped tests

The final full suite collects **105 cases**. Results were actually executed:

| Check | Result |
| --- | --- |
| Windows CPython 3.11.16 | **101 passed, 4 skipped** |
| Windows CPython 3.12.10 | **101 passed, 4 skipped** |
| Windows CPython 3.13.13 | **101 passed, 4 skipped** |
| Windows CPython 3.14.0 | **101 passed, 4 skipped** |
| Ubuntu under WSL, CPython 3.12.3, normal checkout filesystem | **102 passed, 3 skipped** |
| WSL private native tmpfs, targeted FIFO/symlink/descriptor subset | **7 passed**, 35 deselected, no skips |

Windows skips are four POSIX-only cases: FIFO replacement, nonblocking descriptor
handling, and direct/symlink FIFO inputs. Its three symlink path cases executed
successfully. The normal WSL checkout cannot create FIFOs and skips three real
FIFO cases; the descriptor simulation passes there. The native tmpfs run executes
those real FIFO cases successfully. The seven targeted checks reuse existing
tests and are not seven additional unique cases.

Other executed validation:

- Ruff lint and formatting: PASS.
- Wheel and source archive build: PASS.
- Distribution metadata/source/entry-point/license/archive assertions: PASS.
- Built-wheel installation with `--no-index --no-deps` and guarded isolated-import
  smoke checks: PASS on Windows 3.11/3.12/3.13/3.14 and WSL Linux 3.12.
- Windows 3.11 and 3.14 wheel environments were separate runtime-only environments.
- Source archive installation: PASS in a separate Python 3.11 environment using
  a preinstalled compatible setuptools backend and `--no-index --no-build-isolation
  --no-deps`; its installed package passed all smoke assertions and `pip check`.
- `pip check`: PASS in every tested wheel environment and the source-install environment.
- Installed console entry points: PASS on Windows 3.11/3.14 and WSL Linux 3.12;
  isolated module launches across all five runtimes checked terminal/JSON/Markdown,
  UNKNOWN, input errors, help, and version.
- Four GitHub YAML files parsed locally; the requested platform/version matrix
  was checked. This does not validate hosted GitHub execution or every server-side form rule.
- Recorded diagnostic evaluation matches a fresh executed run; the suite guards
  against stale or hand-edited results.

No test coverage percentage, fabricated benchmark, or hosted CI pass is claimed.
Development-only tooling downloads were used; the analyzer still makes no network
requests and has no third-party runtime dependencies.

## 4. Compatibility matrix

| Environment | Status |
| --- | --- |
| Windows Python 3.11, 3.12, 3.13, 3.14 listed above | VERIFIED locally: suite and installed wheel |
| WSL Ubuntu Python 3.12 | VERIFIED locally: suite, wheel, real special files on private tmpfs |
| Hosted/native Ubuntu GitHub Actions | UNVERIFIED: configured, never run |
| Linux Python 3.11, 3.13, 3.14 | UNVERIFIED locally |
| macOS and other unlisted platforms/interpreters | UNVERIFIED |
| Python below 3.11 | UNSUPPORTED by package metadata |

Python 3.11 compatibility is now supported by runtime tests and installation,
not merely AST syntax parsing. It does not establish Linux 3.11 compatibility.
CI retains Ubuntu/Windows × Python 3.11/3.12/3.13/3.14, with a job timeout and
fail-fast disabled so one failing job cannot conceal the rest of the matrix.

## 5. Security findings

### Publication-file review

Reviewed the complete candidate file set, not just already tracked paths (the
repository originally had an empty index). Heuristic scanning checked token
shapes, private-key delimiters, absolute personal paths, and email-like strings.
Seven flagged locations in two test files were reviewed as intentional synthetic
fixtures: dummy PEM headers/payload, a fake AWS-shaped identifier, a JWT-shaped
synthetic payload/signature, and Slack-shaped synthetic strings. Their nearby
tests explicitly create fake data. No actual credential, personal identity,
unexpected email, or private absolute path was found by this scoped review.

This is not a guarantee that automated scanning identifies every secret. The
review covered source, documentation/history, JSON results/schema, synthetic
samples, templates/workflow, license, configuration, tests, and developer tools.
Examples use reserved example domains. No private build log or credential was used.

`.gitignore` excludes environments, interpreter downloads/caches, build outputs,
test scratch directories, `.env` files, common private-key containers, and a
private-log directory. Only intentional sample `.log` files are admitted. Ignore
rules are a guardrail, not a replacement for reviewing every staged file.

### Runtime behavior

All-format synthetic redaction tests passed. They cover escaped quoted values,
CLI secret arguments, Authorization values, URL userinfo/query tokens, npm auth,
AWS/GitHub/Slack/JWT-shaped values, and PEM-shaped input. Tests ensure secret
fixtures actually reach evidence rather than silently disappearing behind caps.
Input-error and formatted reader traceback tests passed without raw OS detail.

The actual runtime has no subprocess, eval, exec, shell-command, or network-client
path. Untrusted logs are read as bounded data and never become commands. Developer
test/evaluation tools run fixed test commands, not log-derived instructions.

Direct FIFOs, symlinks to FIFOs, FIFO replacement, and nonregular descriptors were
rejected without a hang in the supported native-filesystem check. The subprocess
timeout makes a future blocking regression fail rather than hang CI indefinitely.
Regular-file symlinks remain intentionally supported; broken/looping links fail
with a safe input error. The CLI is not a filesystem sandbox or an access-control
allowlist. All agent-created test targets stayed inside this checkout.

Relative paths, spaces, Unicode basenames, and option-like filenames after `--`
were exercised. Input size tests cover the exact byte limit and sentinel behavior,
near-limit content, oversized files, long lines, excessive lines, and unchanged
original bytes. Concurrent file mutation and hostile/unresponsive filesystems
remain outside the safety guarantee.

### Why redaction is best effort

Rules cannot know every credential format, encoding, cookie, proprietary snippet,
personal identifier, malformed/split value, or sensitive path. Masking can also
remove useful diagnostic context. Original logs retain original confidential
content. Reports must be reviewed before sharing. README, SECURITY, issue forms,
and release notes make no guarantee that all confidential information is removed.

## 6. Diagnostic evaluation

Corpus: `samples/evaluation.json`, 22 manually labelled synthetic cases designed
to resemble common CI output. No private or third-party public log was copied.
Run `python tools/evaluate.py`; results are stored in
`docs/diagnostic-evaluation.json` and compared with fresh results by a regression.

| Measure on this corpus | Actual result |
| --- | --- |
| Expected category-list agreement | **21 / 22** |
| Expected source evidence-line agreement | **22 / 22** |
| Emitted evidence grounded in the sanitized original | **22 / 22 cases** |
| Explanation and next-step fields present | **22 / 22 cases** |

The empty-evidence clean-log case is checked against an explicitly empty expected
line list; no evidence is invented. The corpus includes Gradle/Maven, npm,
Python imports, permissions/storage, authentication, GitHub Actions, generic
wrappers, clean/ambiguous logs, unrelated errors, duplicates, ANSI/Unicode,
synthetic credentials, and fake instructions naming nonexistent line 999.

Before the evidence fix, category agreement was 21/22 and evidence-line agreement
21/22. An ambiguous ImportError now retains its real line while remaining UNKNOWN.
All generated log bytes remained unchanged during evaluation, and synthetic
credential assertions passed.

Known misleading result: `quoted-documentation` expects UNKNOWN, but the current
rules report DISK_SPACE for `Documentation example: No space left on device`.
Evidence is real and correctly numbered, but the surrounding meaning is missed.
This remains explicit in the stored results and release notes; no special-case
filter was added merely to improve a tiny evaluation score.

Manual advice review: supported rules suggest investigation of the relevant
coordinates/registry, interpreter environment, permissions, storage/quota, access
scope, or workflow ref/metadata. UNKNOWN asks for more context. This is useful
triage guidance, not proof that following it repairs a build. Advice presence is
not a measured repair rate or validated developer-usefulness score. The quoted
example produces irrelevant storage advice, illustrating the known precision limit.
These counts are corpus agreement, not real-world accuracy, adoption, or benchmarks.

## 7. Remaining risks

- Hosted CI and untested platform/runtime combinations remain unverified.
- A private security reporting channel must be established before release.
- Quoted errors, localization, multiline-only failures, and masking can mislead
  or hide context; category output never proves the root cause.
- Best-effort redaction cannot authorize publication of arbitrary private logs.
- Inputs must be stable local files; symlinks are followed to regular targets.
- Ownership is based on the maintainer's explicit confirmation, not independent
  legal verification. No third-party project source was imported.
- Distribution tooling and checks use assert statements; run release checks with
  normal Python settings, not optimization that strips assertions.

## 8. Publication checklist

Local checklist: `docs/release-checklist.md`. Prepared release notes:
`docs/releases/v0.1.0.md`. Changelog entry remains **Unreleased**.

- [x] Verify Python 3.11 runtime and all available platform suites.
- [x] Run real FIFO/symlink checks on supported Linux storage.
- [x] Review evidence, UNKNOWN behavior, redaction, and misleading diagnoses.
- [x] Confirm MIT intent/rights with the maintainer; preserve the license text.
- [x] Prepare README, schema docs, contribution/security policies, templates, notes.
- [x] Build/inspect artifacts and install wheel/source archives in isolated environments.
- [x] Review the 44-file public candidate set; exclude ignored local material.
- [x] Complete final local staging review before handoff, recording no remotes.
- [ ] Establish a real private security reporting channel before publication.
- [ ] Execute the actual hosted CI matrix and review all outcomes.
- [ ] Obtain explicit approval before any remote, commit/tag release workflow, or publication.

## 9. Readiness verdict

**Local preparation: READY for maintainer handoff.**

**Public GitHub release: NOT READY until hosted CI and private security reporting
are completed and the maintainer explicitly authorizes publication.** Those
external actions were intentionally not performed. No release-readiness claim
relies on fabricated results, an unavailable environment, or perfect redaction.
