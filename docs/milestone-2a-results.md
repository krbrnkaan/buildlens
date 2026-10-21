# Milestone 2A — private GitHub CI verification results

Date: 2026-10-21. Status: **READY — private hosted CI verification completed**.

## Scope and completed actions

- Created `krbrnkaan/buildlens` as an empty **private** repository:
  <https://github.com/krbrnkaan/buildlens>.
- Verified the Private badge and repository settings before attempting a push.
  The authenticated repository API also returned `private: true` and
  `visibility: private` (repository ID `1428854105`).
- Rechecked the approved index: exactly 45 files, all listed in
  `docs/milestone-2a-preflight.md`, no unstaged changes, and a successful
  `git diff --cached --check`.
- Created one unsigned root commit on `main`:
  `7126708d56c7a625dcd09657c1eac78eee2179d8`.
  Message: `Prepare BuildLens v0.1.0 for private CI verification`.
  Author and committer: `krbrnkaan
  <114615439+krbrnkaan@users.noreply.github.com>`.
  Verified zero parents, exactly 45 tracked files, and a clean working tree
  before this results document was added.
- Added only `https://github.com/krbrnkaan/buildlens.git` as `origin`.
  Successfully pushed the explicit refspec `main:refs/heads/main`, with tag following and
  mirror mode disabled and an empty local hooks directory. No tooling refs or
  historical object-store snapshots were selected for upload.

## Hosted outcomes and authentication resolution

The user completed Git Credential Manager sign-in. The existing push completed
successfully (exit code 0); no credentials were shared in chat or added to files.
The first push triggered [CI run #1](https://github.com/krbrnkaan/buildlens/actions/runs/39667229407),
run ID `39667229407`, attempt **1**, for the exact commit above.

GitHub's run API returned `status: completed` and `conclusion: success`.
All eight jobs and every reported step concluded `success`. The actual pytest
summaries, selected Python patch versions, and validation output were read from
each job's hosted logs.

| Hosted OS | Actual CPython | Tests | Job result | Job runtime |
| --- | --- | --- | --- | --- |
| Ubuntu 24.04.5 | 3.11.17 | 105 passed, 0 skipped | [PASS](https://github.com/krbrnkaan/buildlens/actions/runs/39667229407/job/119455360908) | 25 s |
| Ubuntu 24.04.5 | 3.12.15 | 105 passed, 0 skipped | [PASS](https://github.com/krbrnkaan/buildlens/actions/runs/39667229407/job/119455361474) | 24 s |
| Ubuntu 24.04.5 | 3.13.16 | 105 passed, 0 skipped | [PASS](https://github.com/krbrnkaan/buildlens/actions/runs/39667229407/job/119455361475) | 21 s |
| Ubuntu 24.04.5 | 3.14.8 | 105 passed, 0 skipped | [PASS](https://github.com/krbrnkaan/buildlens/actions/runs/39667229407/job/119455361086) | 28 s |
| Windows Server 2025 | 3.11.9 | 101 passed, 4 skipped | [PASS](https://github.com/krbrnkaan/buildlens/actions/runs/39667229407/job/119455361415) | 45 s |
| Windows Server 2025 | 3.12.10 | 101 passed, 4 skipped | [PASS](https://github.com/krbrnkaan/buildlens/actions/runs/39667229407/job/119455361320) | 48 s |
| Windows Server 2025 | 3.13.16 | 101 passed, 4 skipped | [PASS](https://github.com/krbrnkaan/buildlens/actions/runs/39667229407/job/119455361681) | 61 s |
| Windows Server 2025 | 3.14.8 | 101 passed, 4 skipped | [PASS](https://github.com/krbrnkaan/buildlens/actions/runs/39667229407/job/119455361278) | 47 s |

The four Windows skips are POSIX-only checks: direct and symlink FIFO inputs,
FIFO replacement, and nonblocking descriptor handling. Those checks executed on
all four native Ubuntu jobs. No extra Windows symlink skips occurred.

Every job also passed:

- Ruff lint and formatting (27 Python files already formatted).
- Source distribution and wheel build.
- Distribution metadata, version, entry point, MIT license, source-byte and
  archive-content validation.
- Editable installation removal and local wheel installation using
  `--no-index --no-deps`.
- Installed CLI JSON sample and isolated installed-wheel smoke checks covering
  all report formats, UNKNOWN, input errors, help and version.

The run started at `2026-10-21T20:05:11Z` and was recorded complete at
`2026-10-21T20:07:55Z` (2 min 44 s elapsed). The run Usage page reports **4 min
59 s aggregate job runtime**, matching the sum of job timestamps. There were
**zero failed jobs**, no retries, no duplicate manual dispatch, and no local
fixes or additional commits/pushes were necessary.

### Hosted warnings

The summary contains **8 warnings and 4 notices**, not test failures:

- All eight jobs warn that the reviewed checkout/setup-python revisions declare
  Node.js 20 and were forced by GitHub to run on Node.js 24. They succeeded in
  this run. Review current official action revisions and update both the YAML
  and repository allowlist in a separately reviewed follow-up.
- Four Ubuntu notices announce the `ubuntu-latest` migration toward Ubuntu 26.
  These actual jobs used Ubuntu 24.04.5; **Ubuntu 26 is UNVERIFIED** by this run.
  The Ubuntu image revisions were `20261012.334.1` and `20261018.339.1`.
  Windows used image `windows-2025-vs2026`, revision `20261007.264.1`.

## Costs and included allowance

Read the authenticated GitHub billing UI before attempting the push:

- GitHub Free account.
- Actions minutes: **0 used / 2,000 included**, resetting in 11 days.
- Actions storage: **0 GB used / 0.5 GB included**.
- Current Actions billable usage: **$0**.
- Existing account-wide Actions budget: **$0.00 / $0.00**, status
  **Usage blocked**. Included usage alerts were on.

After the successful run, the authenticated billing UI showed:

- **9 min used / 2,000 min included** (baseline before the run: 0 min).
- **$0.05 gross consumed usage**, **$0.05 discounts**, **$0 total billable usage**
  after discounts.
- **0 GB used / 0.5 GB included** Actions storage.

The nine included minutes are the displayed account-counter increase, not a
calculation from aggregate runtime or an invented per-job billing breakdown.
No other workflow was dispatched by this task. Counters can lag and the account
view is not a final invoice or a repository-specific charge attribution.

Billing settings were not changed, no paid usage was enabled, and no payment
authorization was requested or accepted. The existing $0 Actions budget was
preserved. **No charge was reported** at verification time.

## Repository Actions security

Saved and verified the Actions policy:

- Selected actions policy; third-party allowlist contains only
  `actions/checkout@11d5960a326750d5838078e36cf38b85af677262` and
  `actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065`.
- Full-length SHA pinning is required. Broad GitHub-author and Marketplace
  allow options remain off. GitHub's policy also permits actions defined under
  the repository owner's account; this workflow uses only the two listed actions.
- Default workflow token permissions remain read-only; the YAML narrows them
  to `contents: read`. Actions creating or approving pull requests remains off.
- Fork pull request workflows remain off. Actions access from other repositories
  remains off. Existing 90-day log retention was left unchanged.
- Eight matrix jobs, two concurrent, ten-minute per-job timeout. No
  `pull_request_target`, user secrets, artifact uploads, deployment or release
  steps. Checkout uses `persist-credentials: false`.

## Local evidence and remaining risks

The executed local validation is recorded in `docs/milestone-2a-preflight.md`:
Windows Python 3.11–3.14 each had 101 passed / 4 POSIX skips; WSL Python 3.12
had 102 passed / 3 filesystem FIFO skips; a separate native tmpfs run passed
all seven selected FIFO tests. Lint, formatting, distributions and isolated
installation checks passed as detailed there. These are **local results**, not
hosted CI evidence. No runtime source or tests were changed during this step.

- Hosted compatibility is verified only for the eight recorded combinations,
  selected patch versions, and runner images. macOS, Ubuntu 26, other Python
  implementations, and all other environments remain UNVERIFIED by this run.
- Redaction remains best effort. Do not submit real private logs or credentials
  to issues, tests, CI output or this repository.
- CI installs development/build tools from package registries; SHA-pinned
  actions do not eliminate dependency supply-chain risk.
- Private repository visibility is access control, not a confidential disclosure
  channel for every collaborator. Follow `SECURITY.md`.
- GitHub Private Vulnerability Reporting must be enabled and verified if a
  separately approved public launch happens later. It is not claimed enabled now.
- Local tooling snapshot refs and historical unreachable blobs were excluded by
  the root commit and explicit branch refspec. Never mirror this local object
  store or upload local workspace archives.

## Verdict and boundaries

**READY: Milestone 2A private hosted CI verification completed.** All eight
approved combinations actually passed on GitHub. This is not authorization for
public visibility or a public release. The action-runtime warning and moving
runner image labels remain follow-up maintenance risks.

Post-push API inspection confirmed that the remote still has private visibility,
only `refs/heads/main`, the exact initial root commit (zero parents), and tree
`2d6bc826ec120dbf48d779214263c26af28d5047`. That tree matches the local approved
45-file commit. No tooling snapshot refs or excluded files were uploaded.

No release, package publication, visibility change, billing change, collaborator
invitation or public launch was performed. This results document is local and
outside the approved 45-file initial upload; it has not been committed or pushed.
