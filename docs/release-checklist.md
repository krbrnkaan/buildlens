# v0.1.0 publication checklist

This is a preparation document, not authorization to publish. No remote, tag,
release, or push is created by the local verification tools.

## Local gates

- [x] Maintainer confirmed control of the workspace's rights and intent to use MIT.
- [x] Preserve the MIT text and project copyright notice without inventing author identities.
- [x] Keep package and CLI version 0.1.0, and JSON schema version 1.0.
- [x] Add changelog, draft release notes, issue forms, and documented limits.
- [x] Execute Python 3.11 tests rather than relying only on syntax parsing.
- [x] Exercise real Linux FIFOs on a supported filesystem in a private namespace.
- [x] Recheck the final test, artifact, staging, and privacy results against the milestone 1.6 report.
- [x] Review every staged path and confirm no ignored environments/caches/private files are included.

## Maintainer actions before any public release

- [ ] Explicitly approve creating the intended public repository and publication destination.
- [ ] Establish a private security contact or enable private vulnerability reporting;
      document the working channel before asking users to disclose security issues.
- [ ] Run the actual hosted Ubuntu/Windows × Python 3.11/3.12/3.13/3.14 matrix.
- [ ] Review all failures and skips; do not turn an unavailable environment into a PASS.
- [ ] Review the known quoted-example false positive and redaction limitations in the release notes.
- [ ] Verify the exact wheel/source archives and final version again after any change.
- [ ] Create the initial commit/tag and publish only after explicit approval.

The milestone 1.6 report records the executed local checks. Human ownership
confirmation is not an independent provenance or legal audit. No public release
should claim a perfect confidentiality filter or verified universal compatibility.
