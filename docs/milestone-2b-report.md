# Milestone 2B — final public release preflight

Date: 2026-10-21. Candidate: **BuildLens 0.1.0**, JSON schema **1.0**.

**NOT READY for public release yet.** The initial private commit passed hosted
CI, but the modified source and action pins need a new eight-job run. Public
visibility, Private Vulnerability Reporting (PVR), a release tag and release
publication still require separate approval. No remote changes, commits, pushes,
paid usage, releases or package uploads were performed during this milestone.

## 1. Findings and changes

### Release blockers

1. **The changed candidate has not run on GitHub.** Run 39667229407 passed all
   eight jobs for initial commit `7126708d56c7a625dcd09657c1eac78eee2179d8`.
   That evidence does not validate these local edits. All eight jobs must rerun.
2. **The remote action allowlist needs an approved update.** Its last verified
   policy allows only the two old action SHAs, plus owner-local actions under
   GitHub's selected-actions policy. New SHA pins cannot run under that old
   allowlist. Do not relax the policy to all actions to bypass this gate.
3. **PVR is not enabled or verified while the repository is private.** It must be
   enabled and checked after an approved public visibility change and before
   announcement. There is no invented security email, response SLA or bounty.
4. **No public publication approval exists.** This report proposes an exact
   sequence; it does not authorize any external action.

### Documentation and historical evidence

README, contributing guide, changelog, release notes, security policy and checklist
now state that the private repository exists and the initial hosted run passed.
Historical milestone reports retain their original results with prominent
supersession notices; their old absent-remote/unrun-CI statements describe those
earlier checkpoints only. No historical test count was rewritten as a new result.
macOS and Ubuntu 26 remain **UNVERIFIED** everywhere in current release messaging.

### Narrow diagnostic correction

The synthetic line `Documentation example: No space left on device` previously
created a DISK_SPACE diagnosis. A case-insensitive, start-of-line label match
(allowing leading whitespace) now treats explicitly labelled documentation
examples as non-actionable. Their actual text and original source line are
retained as UNKNOWN evidence when no supported failure is present.

This does not skip later lines or suppress an error merely because it contains
quotes, the word documentation, or the label later in an operational error.
The architecture, CLI, advice, input limits, schema version, and runtime
dependencies are unchanged. Five new regression cases cover the explicit label,
following real failure, quoted OSError, documentation-build failure, and a label
embedded within an operational error. The existing evaluation test now also
requires all expected categories and evidence lines to agree.

The two new negative cases failed before the production change (DISK_SPACE was
returned); three operational guard cases already passed. After the correction,
all five and the recorded-evaluation check passed. The same original 22-case
corpus now has **22/22 category agreements and 22/22 line agreements**, with
grounded evidence and advice throughout. Only `quoted-documentation` changed
classification; the other 21 recorded results are unchanged. This is a tiny
synthetic regression corpus, not measured real-world accuracy.

Limit: this is a literal convention. Unlabelled, fenced, or timestamp-prefixed
examples can still match. A real error printed under this exact example label
can be missed. The fix makes no claim to understand arbitrary documentation.

## 2. Official action replacements

The official GitHub release APIs, tag references and files at the exact commit
were inspected read-only before editing the workflow:

| Action | Previous pin | Proposed official release and full commit |
| --- | --- | --- |
| checkout | `11d5960a326750d5838078e36cf38b85af677262` | [v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1), `3d3c42e5aac5ba805825da76410c181273ba90b1` |
| setup-python | `a26af69be951a213d495a4c3e4e4022e16d87065` | [v7.0.0](https://github.com/actions/setup-python/releases/tag/v7.0.0), `5fda3b95a4ea91299a34e894583c3862153e4b97` |

Both official tag refs resolve directly to these commits. Both `action.yml`
files declare **node24**, and both LICENSE files contain MIT terms. Their
official README files require runner v2.327.1 or later; the previous hosted run
used v2.338.0. These are hosted-runner updates, not support for arbitrary old
self-hosted runners. No vendor action implementation was copied into BuildLens.

The setup-python documentation recommends `contents: read`. The workflow retains
only `contents: read`, `persist-credentials: false`, shallow checkout, no cache
configuration, two concurrent jobs and ten-minute job timeouts. It adds no
secrets, write scopes, OIDC, artifact upload, deployment, privileged PR event or
untrusted expression interpolation. Existing repository token/PR/fork/access
restrictions must remain intact. Verification of tag provenance and declared
runtime is not a complete independent audit of vendor bundles or dependencies.

## 3. Actual validation results

### Established hosted baseline, before these edits

[Run 39667229407](https://github.com/krbrnkaan/buildlens/actions/runs/39667229407)
completed successfully on its first attempt: all eight jobs and all reported
steps succeeded. Ubuntu 24.04.5 passed 105 tests per Python version; Windows
Server 2025 passed 101 with four POSIX-only skips per version. Lint, formatting,
build, archive metadata checks and installed-wheel smoke checks passed in each.
See [the reviewed 2A results](milestone-2a-results.md) for exact patch versions,
job URLs and usage. **No new hosted run was started in Milestone 2B.**

### Local candidate

| Environment | Executed result |
| --- | --- |
| Windows Python 3.11.16 | 106 passed, 4 POSIX skips |
| Windows Python 3.12.10 | 106 passed, 4 POSIX skips |
| Windows Python 3.13.13 | 106 passed, 4 POSIX skips |
| Windows Python 3.14.0 | 106 passed, 4 POSIX skips |
| WSL Ubuntu Python 3.12.3, checkout filesystem | 107 passed, 3 unsupported-FIFO filesystem skips, using `--capture=sys` |
| WSL native temporary tmpfs FIFO/descriptor/symlink checks | 7 passed, 40 deselected, no skips |
| Windows and WSL Ruff lint / format check | PASS |
| New workflow on GitHub, all eight combinations | **NOT RUN — requires approval** |
| macOS / Ubuntu 26 / other environments | **UNVERIFIED** |

The suite contains 110 collected test cases after five meaningful additions;
repeated interpreter runs are not additional unique tests. Three Windows runs
finished before a 60-second orchestration timeout prevented a fourth result;
the complete Python 3.14 suite was then run separately and passed. The default
WSL pytest file-descriptor capture failed before collection with a temporary-file
`FileNotFoundError`, including on a sequential retry with a separate temporary
directory. `--capture=sys` allowed the full suite to execute successfully.
Native tmpfs FIFO checks used the normal capture mode and passed. The private
mount was cleaned up (`mountpoint` returned 32: not mounted). These are local
harness/filesystem limitations, not claimed passing default WSL checks.

Initial lint found two overlong newly added lines; formatting was corrected and
lint/format checks passed afterwards. No coverage percentage is claimed.

`python -m build` and `python tools/check_distribution.py` passed: wheel/sdist
metadata, version, MIT license, entry point, runtime dependency declarations,
source bytes and archive path/content checks were verified. The build emitted
benign warnings about the unused `.github/*.md` manifest glob and disabled
byte-compilation; neither prevented either artifact from building.

Local wheel installation using `--no-index --no-deps`, isolated-import smoke
checks for all formats/UNKNOWN/input errors/help/version, and `pip check` passed
in clean Windows Python 3.11 and 3.14 environments and a clean WSL Python 3.12
environment. WSL's normal venv creation initially failed because `ensurepip` is
unavailable; the existing project-local pip successfully installed into the
isolated target environment via `--python`, without installing system software
or injecting development packages into the smoke process. These successful
wheel checks do not mean ordinary `venv` creation works on this WSL installation.

Final artifacts are local validation candidates only. Rebuild and approve exact
SHA-256 digests at the final verified release commit; no archive was uploaded.
An attempted final rebuild with `--no-isolation` failed because the development
environment does not contain setuptools. The supported default isolated build
provides its declared backend; no global package installation is needed.

## 4. Security, privacy, licensing and packaging review

- Reviewed the 45 tracked files plus the local 2A report and this proposed report.
  Secret/token/PEM/email/private-path scans found only established synthetic test
  fixtures, reserved `example.invalid` addresses, and the already approved
  GitHub no-reply commit identity. No actual credential, home/checkout absolute
  path, payment details or private log was identified in the publication payload.
  Pattern scanning and human review are not proof that every confidential value
  can be detected.
- The local 2A results report was explicitly reviewed: it contains commit/run
  identifiers, test results, aggregate included-minute usage and discounted $0
  billable usage. It contains no payment method, contact email, local private
  path or credential. Proposed inclusion still requires approval. The sdist's
  recursive docs manifest includes it; it must not be treated as automatically
  approved merely because a build contains it.
- Existing all-format redaction, exception-output, false-positive, oversized
  input, control-sequence, symlink and untrusted-instruction checks remain in
  the full suite. Runtime code has no command-execution or network imports.
  No commands from logs were executed. Redaction remains **best effort**:
  personal information, paths, proprietary text and unknown secret forms can
  remain. Review every generated report before sharing.
- MIT text and version 0.1.0 remain unchanged. The owner previously confirmed
  control of rights and MIT intent; this is not independent legal verification.
  No new runtime or development dependency was added. Runtime remains standard
  library only; action licenses were checked as above. No third-party source was
  imported or vendored.
- Preserve the previous no-mirror policy: local tooling snapshot refs and
  unreachable historical blobs are not part of the approved branch history.
  Never upload `.git`, workspace archives, ignored environments, caches or real logs.

## 5. Confidential disclosure plan

Current private evaluation uses the maintainer's existing verified private
conversation; a private repository issue is visible to its collaborators and is
not automatically a confidential disclosure channel. Do not invent an email.

For a separately approved public launch, follow
[GitHub's PVR configuration instructions](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository):
after the approved visibility change, enable PVR under Settings → Advanced
Security, check Security → Advisories → Report a vulnerability and the form,
and verify access from an eligible non-maintainer account before announcing.
Do not submit a fake advisory. Record the verified destination only after it
works. The currently documented Security link is a planned destination, not a
claim of enabled reporting. Stop announcements if verification fails.

Request the affected version, OS/Python versions, impact summary and minimal
synthetic reproduction. Acknowledge through the private advisory, agree on
participants, reproduce privately, coordinate a fix and disclosure timing, and
avoid real credentials/logs. No SLA, bounty or confidentiality guarantee is
promised. Use the verified private fallback if GitHub reporting is unavailable.

## 6. Files and exact proposed publication sequence

Changed tracked files (16): `.github/workflows/ci.yml`, `CHANGELOG.md`,
`CONTRIBUTING.md`, `README.md`, `SECURITY.md`, `docs/diagnostic-evaluation.json`,
`docs/milestone-report.md`, `docs/milestone-1.5-report.md`,
`docs/milestone-1.6-report.md`, `docs/milestone-2a-preflight.md`,
`docs/release-checklist.md`, `docs/releases/v0.1.0.md`, `samples/evaluation.json`,
`src/buildlens/analyzer.py`, `src/buildlens/rules.py`, `tests/test_release.py`.
New local reports (2): `docs/milestone-2a-results.md`, `docs/milestone-2b-report.md`.
Proposed branch payload: the same 45 original paths plus those two reports,
**47 files total**. No files are staged or committed by this milestone.

1. **Approval A, private verification only:** approve the reviewed 18-file diff
   and inclusion of both reports, one new local commit on `main`, the two exact
   new action allowlist entries above, and an explicit `main:refs/heads/main`
   push to the still-private `krbrnkaan/buildlens`. Use the previously approved
   public no-reply attribution and empty local hooks; do not mirror refs or push
   tags. Recheck private visibility, the final diff, included minutes and the
   existing $0 Actions budget before any run. Do not enable paid usage.
2. Update the allowlist to the two new pins without broadening workflow token
   access, then push once. The push triggers all eight Ubuntu/Windows × Python
   3.11/3.12/3.13/3.14 jobs: full tests, lint, formatting, build, distribution
   validation and installed-wheel smoke. A manual duplicate run is unnecessary.
   Inspect warnings, skips and costs. Stop if payment or broader access is required.
3. Record the exact new SHA/run outcome locally. If documentation or any other
   file must change after that run, review and approve that additional commit
   and push, and validate its exact release commit too. No old run may be
   presented as verification of a different tree.
4. **Approval B, separate public launch:** after the final candidate passes,
   request approval for the visibility change and PVR setup/verification.
   Complete the disclosure gate before any release announcement. If the policy
   needs a verified-link edit, review/approve and verify that final commit before
   tagging. Recheck all reachable history and files for public suitability.
5. **Approval C, exact release:** approve `v0.1.0` at the verified final SHA, the
   final release-note text, and the exact wheel/sdist SHA-256 digests. Create only
   that tag and GitHub release, and upload only those two artifacts and their
   checksum file. No package registry upload is included; PyPI requires a
   separate request. No release or tag is created during this preflight.

The initial 2A run reported nine included minutes and $0 billable usage; no 2B
hosted job has consumed minutes. This is historical accounting, not a promise
about future allowance. Recheck the account before any approved rerun.

## 7. Verdict and residual risks

**NOT READY for public release.** Local preparation does not replace fresh hosted
verification of the changed source/workflow or the PVR activation gate. The
candidate is prepared for a separately approved private commit/push and matrix
run; the executed local artifact checks passed.

Remaining risks: deterministic English signatures can miss or misclassify logs;
explicit labels are not semantic context; redaction cannot remove all private
information; development dependencies are not a reproducible lockfile; vendor
actions and moving runner images retain supply-chain/compatibility risk; macOS
and Ubuntu 26 remain unverified. No public release, package upload, remote
configuration change or billing change was performed.
