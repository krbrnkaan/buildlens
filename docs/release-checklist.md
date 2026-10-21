# Release verification procedure

This procedure does not authorize publication by itself. Release execution must
stay within the maintainer's explicit approval; package registry publication is
separate. Record actual completion evidence on the GitHub Release and in the
local release report. Do not mark an unrun check as passing.

## Established v0.1.0 prerequisites

- The maintainer confirmed control of rights and MIT intent. Preserve the MIT
  text and copyright notice; this is not independent legal provenance verification.
- Package/CLI version is 0.1.0; JSON schema is 1.0; runtime dependencies are empty.
- The maintainer approved public exposure of the reviewed Git history, no-reply
  identity, historical account/billing summaries and existing Actions logs.
- The repository is public and GitHub Private Vulnerability Reporting is enabled.
  On 2026-10-22 the maintainer independently confirmed form access from a separate
  account with no repository maintainer/admin role. No fake report was submitted.
- The maintainer authorized the final necessary documentation commit/push,
  all eight CI jobs, tag v0.1.0, a GitHub Release and exactly three uploaded
  assets: reviewed wheel, source archive and SHA-256 checksum file. No PyPI upload.

## Execute before publishing

1. Review and explicitly stage only necessary release documentation. Exclude
   local ledgers/reports, private logs, snapshots, `.git`, environments and caches.
   Review added content for accidental private data and preserve best-effort
   redaction and unverified macOS/Ubuntu 26 limitations.
2. Confirm public visibility, enabled PVR and the exact reporting link in
   SECURITY.md. Keep confidential receipt/reproduction/disclosure coordination;
   no invented email, SLA or bounty. Stop if the security gate fails.
3. Verify sufficient included Actions allowance and the existing $0 spending
   guard; do not enable paid usage or alter billing. Preserve reviewed full-SHA
   actions, read-only token permissions and the current matrix/timeouts.
4. Commit and push the reviewed file set only. Run all eight Ubuntu/Windows ×
   Python 3.11/3.12/3.13/3.14 jobs on that exact final commit. Inspect every job,
   test count, skip, warning and package check; stop on validation failure.
5. Export only that verified commit into a clean directory inside BuildLens.
   Build wheel/sdist there, inspect all archive members and metadata/license/
   source bytes, and verify isolated wheel installation. Compare source archive
   contents against the exported commit, allowing generated packaging metadata.
   Recursive docs manifests must not collect untracked local reports.
6. Calculate SHA-256 for the final wheel and source archive; create
   `SHA256SUMS.txt` containing only those two filenames/digests. Freeze these
   exact bytes; no rebuild or file edit after hashing without revalidation.
7. Confirm tag v0.1.0 resolves to the CI-verified commit, not a later main tip.
   Do not use a mirror push or publish local tooling refs. Record the exact SHA
   and final CI URL in the release body.
8. Publish the approved GitHub Release with only the reviewed wheel, sdist and
   checksum file. Verify public state, tag target, asset names/sizes and downloaded
   bytes/digests. GitHub's automatic source-code links are separate from the three
   uploaded assets and are not the built sdist.
9. Record the release URL, tag/SHA, actual CI outcomes, digests, asset inventory,
   observed billing status and remaining limitations in the local release report.
   Stop; no additional feature work or registry publication is authorized.

If a required check fails, stop without publishing. Do not repair a failed final
candidate with an unverified post-CI change. Any revised candidate needs review
and a fresh exact-commit CI run.
