# Milestone 2A — private GitHub CI preflight

Date: 2026-10-21. BuildLens **0.1.0**, report schema **1.0**.

**READY for private upload, subject to explicit approval and the external
preconditions below.** Local preflight passed. **GitHub-hosted CI has NOT RUN**;
no hosted combination is reported as passing. This is not public-release approval.

No GitHub repository, commit, remote, push, upload, visibility change, release,
or external configuration was created during this task. GitHub account/vendor
metadata and official documentation were read only. No unrelated local project
was inspected. All local project work stayed inside this checkout.

## 1. Proposed repository and upload

- Owner: **krbrnkaan**, confirmed through the authenticated GitHub connector and
  public account metadata. No organization or unrelated repository was inspected.
- Repository name: **buildlens**. Proposed destination: `krbrnkaan/buildlens`.
- Visibility: **private**, remaining private throughout CI verification.
- Branch: **main**. Do not auto-create a README/license/gitignore on GitHub.
- Proposed history: **one new root commit**, message
  `Prepare BuildLens v0.1.0 for private CI verification`, from the reviewed index.
- Proposed author and committer: `krbrnkaan`, using the GitHub-format no-reply
  address `114615439+krbrnkaan@users.noreply.github.com`. This follows the verified
  account ID/login and creation-era format; it is commit attribution, **not a
  vulnerability-reporting contact**. No real-name or private-email identity will
  be inherited from machine-global Git settings.

The no-reply format is documented in [GitHub's email reference](https://docs.github.com/en/account-and-profile/reference/email-addresses-reference#your-noreply-email-address).
Commit creation and this identity are part of the approval request. No commit
hash exists yet. Repository-name availability, create/push permissions, native
Git authentication, and included Actions allowance remain external preconditions.
If the target already exists, stop rather than altering an existing repository.
Git is available; the GitHub CLI is not installed. No CLI installation or account
credential configuration is authorized by this local preparation alone.

### Exact proposed file set

The original **44 staged files** were reviewed; this new report makes **45**.
The workflow and SECURITY policy are the only original files changed in this
milestone. No analyzer behavior or test fixtures were changed.

```text
.gitattributes
.github/ISSUE_TEMPLATE/bug_report.yml
.github/ISSUE_TEMPLATE/config.yml
.github/ISSUE_TEMPLATE/feature_request.yml
.github/workflows/ci.yml
.gitignore
AGENTS.md
CHANGELOG.md
CONTRIBUTING.md
LICENSE
MANIFEST.in
README.md
SECURITY.md
docs/diagnostic-evaluation.json
docs/json-schema.md
docs/milestone-1.5-report.md
docs/milestone-1.6-report.md
docs/milestone-2a-preflight.md
docs/milestone-report.md
docs/release-checklist.md
docs/releases/v0.1.0.md
docs/report.schema.json
pyproject.toml
samples/adversarial.log
samples/evaluation.json
samples/lockfile.log
samples/mixed.log
samples/permissions.log
samples/unknown.txt
src/buildlens/__init__.py
src/buildlens/__main__.py
src/buildlens/analyzer.py
src/buildlens/cli.py
src/buildlens/models.py
src/buildlens/reader.py
src/buildlens/redaction.py
src/buildlens/rules.py
src/buildlens/render.py
tests/test_buildlens.py
tests/test_hardening.py
tests/test_release.py
tools/check_distribution.py
tools/check_linux_fifo.sh
tools/evaluate.py
tools/smoke_wheel.py
```

No virtual environments, local Python distributions, caches, `.env` files, private
logs/keys, build outputs, Git object-store archives, or native credentials are
included. Distribution artifacts are built inside CI, not uploaded from local
`dist/` as part of this initial push.

## 2. Git history and sensitive-data audit

The branch is unborn: there are **no commit objects or commit author records**,
and no configured remote. No previous commit history would be uploaded.

The repository is not an empty object store. Local tooling has tree snapshot refs
under `refs/codex/`; previous staging also left unreachable blobs. Object scanning
found **three unreachable historical blobs containing an old absolute checkout
path**, with no user-home path identified. They are outside the current reviewed
index and are not proposed upload content. Tooling refs were not deleted or rewritten.

After approval, create a root commit from only the 45 reviewed files, inspect
that commit's reachable file list and identity, then push **only**
`main:refs/heads/main`. Do not use mirror/broad ref pushes, copy `.git`, upload the
object store, attach local workspace archives, or push tooling refs. No old blobs
become parents of the proposed root commit. Recheck these conditions immediately
before any push; unexpected existing history requires another review.

All original staged content was scanned for token shapes, private-key delimiters,
absolute personal paths, and email-like identifiers. Seven flagged locations in
two test files are deliberate synthetic PEM/AWS/JWT/Slack-shaped fixtures and
their assertions. No unexpected credential, private email, personal identity, or
absolute private path was found in the proposed source files. The public GitHub
handle/no-reply attribution in this proposal is intentional, not a private contact.

The final staged set also receives whitespace, ignored-path, and sensitive-pattern
checks. These are scoped review results, not a guarantee that scanning can detect
every secret. Original logs were synthetic; no private logs or real credentials
were used, and log contents never become commands.

## 3. License and dependency review

- BuildLens remains MIT. The maintainer explicitly confirmed rights/control and
  MIT intent in milestone 1.6; that confirmation persists. This is not an
  independent legal/provenance audit.
- Runtime dependencies: **none** beyond Python's standard library. AST/import
  inspection found no external runtime imports, eval/exec/compile calls, or
  subprocess/network imports in the runtime package.
- Installed development metadata was reviewed: build/pytest/Ruff/iniconfig/pluggy/
  pyproject-hooks/pip declare MIT; Colorama declares BSD; Pygments BSD-2-Clause;
  packaging Apache-2.0 OR BSD-2-Clause. The setuptools build backend is separate
  development tooling; dependency implementations are not bundled in BuildLens.
- Both official Actions declare MIT at their verified pinned revisions. No vendor
  source was copied into this project. Wheel/source checks verify the MIT license,
  metadata, entry point, package bytes, and exclusion of local environments.
- Build/test requirements are version ranges rather than a hash-locked dependency
  set. Public package-index supply-chain risk and version drift remain; pinning
  the Actions does not eliminate these risks or constitute a security/legal audit.

No conflicting runtime dependency redistribution was observed. Tests, docs,
synthetic data, templates, and tooling were reviewed as part of the candidate set.

## 4. Executed local validation

Fresh results for the **105-case** suite:

| Environment | Actual result |
| --- | --- |
| Windows Python 3.11.16 | **101 passed, 4 skipped** |
| Windows Python 3.12.10 | **101 passed, 4 skipped** |
| Windows Python 3.13.13 | **101 passed, 4 skipped** |
| Windows Python 3.14.0 | **101 passed, 4 skipped** |
| WSL Ubuntu Python 3.12.3, normal checkout filesystem | **102 passed, 3 skipped** |
| Native Linux tmpfs in private namespace, targeted special-file subset | **7 passed**, 35 deselected |

Windows skips four POSIX-specific cases. The normal WSL filesystem skips three
real-FIFO cases because it cannot create FIFOs; all real FIFO/symlink/descriptor
checks pass on the private native filesystem inside the checkout. This subset
reuses existing cases and is not seven additional unique tests.

Also executed successfully:

- Ruff lint and formatting on Windows and WSL Linux.
- Wheel and source archive build and `tools/check_distribution.py` assertions.
- Installed-wheel smoke checks and `pip check` on all five tested runtimes above;
  Windows 3.11/3.14 use separate clean runtime environments.
- Source-archive installation in a separate Windows Python 3.11 environment with
  its compatible preinstalled backend, plus installed smoke checks and `pip check`.
- Four GitHub YAML files parsed locally; matrix, safe triggers, read-only token,
  immutable action refs, and disabled credential persistence asserted.
- Full tests include all-format redaction, source-line integrity, UNKNOWN cases,
  non-execution of embedded commands, limits, relative/Unicode/symlink paths, and
  reproducibility of the 22-case diagnostic evaluation.

The known quoted-documentation false positive remains documented: category
agreement is 21/22 on that tiny synthetic corpus, with all expected line positions
correct. It is not a real-world accuracy benchmark. No hosted CI result or
coverage percentage is inferred from local success.

## 5. Planned GitHub Actions jobs

Eight matrix jobs: each combination of `ubuntu-latest` / `windows-latest` with
Python **3.11, 3.12, 3.13, 3.14**. All eight hosted outcomes are **NOT RUN**.
Local WSL 3.12 is not a native GitHub Ubuntu result. Linux 3.11/3.13/3.14, macOS,
and other unlisted local environments remain UNVERIFIED; Python below 3.11 is
UNSUPPORTED. No requested matrix combination is omitted or claimed unsupported
merely because it has not been run yet.

Every job will:

1. Check out the approved commit and select its matrix Python.
2. Install the project with development tooling from the public package index.
3. Run pytest, Ruff lint, and formatting checks.
4. Build wheel/source artifacts and assert metadata, license, and package contents.
5. Remove the editable package and install the built wheel with no index/dependencies.
6. Exercise the console CLI and isolated installed-wheel smoke checks for all
   formats, UNKNOWN/input errors, help, and version.

Maximum two jobs at once, fail-fast disabled, ten-minute job timeout. Triggers:
`push`, `pull_request`, `workflow_dispatch`. The first approved push containing
the workflow will normally trigger the eight jobs; avoid a redundant manual
dispatch unless a rerun is needed.

## 6. Security configuration

Local workflow changes:

- `permissions: contents: read`; unspecified token permissions are not requested.
- `actions/checkout@11d5960a326750d5838078e36cf38b85af677262` (verified official v4 ref).
- `actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065` (verified official v5 ref).
- Official repository commit APIs and license text were checked read-only.
- Checkout uses `persist-credentials: false` and `fetch-depth: 1`.
- No `pull_request_target`, user-supplied secrets, OIDC, deployments, publishing,
  artifact-upload action, cache upload, self-hosted runner, or untrusted event-text
  interpolation into shell commands. GitHub's automatic token remains read-only.

These mitigate exposure; they do not prove that Actions or downloaded dependencies
are free from supply-chain issues. See [GitHub's workflow security guidance](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions).

After approval, configure only this private repository's Actions access: permit
the two reviewed official pinned Actions, use read-only default workflow
permissions, and do not allow Actions to create/approve pull requests. Respect
any stricter existing account policy rather than relaxing it. No account secrets,
environments, webhooks, Pages, billing purchases, or paid runners are proposed.

Before the first push/run, verify that included Actions allowance is sufficient
and that no paid usage is required. If quota, entitlement, authentication, or
required policy is unclear, stop and ask; do not buy capacity or raise spending
limits. Private CI may consume the account's shared included allowance, which has
not been inspected or promised available here.

## 7. Confidential disclosure

SECURITY.md now defines the private-phase process: use the existing verified
private conversation with the maintainer; share only impact, versions, and a
minimal synthetic reproducer; confirm recipients before sharing any sensitive
details; coordinate fixes privately. A private-repository issue is not confidential
from its collaborators. Public issues, PRs, and CI logs are not private reports.
No contact email, bounty, or response deadline is invented.

When the repository becomes public, **GitHub Private Vulnerability Reporting must
be enabled and its reporting form verified before announcing the release**.
GitHub documents this feature for public repositories; it is not claimed enabled
or available for the proposed private repository. See [the official configuration
instructions](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository).
Visibility changes and public-phase configuration require a later, separate approval.
Best-effort redaction never guarantees removal of confidential information.

## 8. Exact approval request — no actions performed yet

Approval would authorize only:

1. Verify the proposed personal-account destination and included Actions
   entitlement, then create the empty **private** `krbrnkaan/buildlens` repository.
   If the name exists or policy/permissions differ, stop for direction.
2. Configure the repository-scoped Actions security settings described above,
   without changing account billing, adding secrets, or relaxing stricter policy.
3. Create the one initial local root commit from these **45 reviewed files**,
   using the proposed public no-reply author/committer identity, and verify its
   reachable files/metadata. Use command-scoped identity, disable signing for this
   unsigned initial commit, and use an empty hooks directory inside this checkout
   so no inherited hook can execute unrelated local code. Do not change global
   Git settings. Stop if unexpected history or content appears.
4. Add this repository's exact GitHub HTTPS origin locally and push **only main**.
   Use secure existing authentication or an approved interactive login; never
   print/store a plaintext token in source, commands, or logs. Do not copy `.git`,
   mirror refs, or upload local distribution/workspace archives.
5. Allow the first push to run the eight hosted matrix jobs using included
   allowance only, then read their statuses/logs, report actual outcomes, and
   prepare any necessary local fixes for review.

Approval would **not** authorize public visibility, releases, tags, package
publication, deployments, collaborator invitations, external integrations,
additional pushes, paid usage, or changes to unrelated repositories. Any changed
upload content or required broader action needs review and renewed approval.

**Current gate: waiting for explicit permission.** The reviewed local payload is
READY for private upload. GitHub-hosted CI verification is pending and no public
release readiness is asserted.
