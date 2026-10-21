# v0.1.0 publication checklist

This checklist is not authorization to commit, push, change visibility, publish
a release, upload packages, or change external settings.

## Established evidence

- [x] Maintainer confirmed ownership/control of rights and intent to use MIT.
- [x] Preserve MIT text and project copyright; no invented contributor identities.
- [x] Package/CLI version 0.1.0; JSON schema 1.0; no runtime dependencies.
- [x] Private repository `krbrnkaan/buildlens` and initial 45-file root commit exist.
- [x] Initial commit `7126708` passed all eight hosted Ubuntu/Windows × Python
      3.11/3.12/3.13/3.14 jobs in run 39667229407, first attempt.
- [x] Reviewed the local milestone 2A results report for proposed public inclusion:
      commit/job identifiers, synthetic test results and aggregate usage only;
      no credentials, payment details or private local paths.
- [x] Reproduce and fix the explicit documentation-example false positive with
      regression tests, without suppressing ordinary quoted errors.
- [x] Verify official Node.js 24 action replacement tags, full commit SHAs,
      declared runtime, licensing, runner minimum and read-only permission needs.

## Before an approved private push

- [ ] Review the exact final file list/diff, including both new milestone reports,
      source, tests, evaluation output, documentation, and workflow pins.
- [x] Complete and review the final local tests, lint, format, build, archive
      inspection and isolated wheel checks recorded in milestone 2B.
- [ ] Obtain explicit approval for the reviewed commit/push and repository Actions
      allowlist update. No broad ref pushes, tags, tooling snapshots or ignored files.
- [ ] Verify the repository is still private and sufficient included allowance
      remains with the $0 Actions budget intact; do not enable paid usage.
- [ ] Replace the external action allowlist with the two exact reviewed new SHAs
      before pushing the changed workflow; preserve read-only token and other restrictions.
- [ ] Run all eight hosted jobs on the exact candidate commit; inspect every
      failure, skip and warning. The old passing run does not validate these edits.
- [ ] Record the new run URL, SHA, results and usage without claiming unrun checks.
      Review and approve any further documentation commit/push; verify its final
      commit as well. Do not silently add a post-CI change to the release tag.

## Before public visibility and announcement

- [ ] Obtain separate explicit approval for making the existing repository public,
      enabling private vulnerability reporting, creating tag `v0.1.0`, and the
      intended GitHub release assets. Package registry publication is separate.
- [ ] Review all reachable release history, author identity, file contents and
      exact wheel/sdist; compare the release tag to the verified commit.
- [ ] After the approved public visibility change, enable GitHub Private
      Vulnerability Reporting in Settings → Advanced Security. Verify the
      Security → Advisories → Report a vulnerability link and form, including
      access from an eligible non-maintainer account, before announcements.
      Do not submit a fake security advisory. If unavailable, stop the launch
      and arrange a verified confidential channel; do not imply PVR is enabled.
- [ ] Document the verified reporting destination and coordinate private receipt,
      reproduction, fix and disclosure with reporters. No invented email, SLA or bounty.
- [ ] Keep macOS/Ubuntu 26 UNVERIFIED and redaction best effort in release messaging.
- [ ] With explicit approval, create the exact tag and GitHub release, attaching
      only the reviewed wheel/sdist and their SHA-256 digests. Do not upload the
      checkout, `.git`, environments, tooling snapshots or private input logs.

Historical reports describe their original checkpoints. See milestone 2B for
the current preflight and remaining gates. Ownership confirmation is not an
independent legal/provenance audit; synthetic agreement is not real-world accuracy.
