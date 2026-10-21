# Security policy

BuildLens 0.1.x is an early CLI. `krbrnkaan/buildlens` is public and GitHub Private
Vulnerability Reporting is enabled. Its public entry point was checked on
2026-10-22. The maintainer independently confirmed that the reporting form opens
under a separate account with no repository maintainer or administrative
permissions. No fake report was submitted. No contact email is specified.
There is no guaranteed response time or formal security support commitment.

## Confidential disclosure

Use GitHub's [Report a vulnerability](https://github.com/krbrnkaan/buildlens/security/advisories/new)
link from the [Security page](https://github.com/krbrnkaan/buildlens/security).
GitHub sign-in is required. The entry point is visible publicly, and independent
non-maintainer form access was confirmed by the maintainer on 2026-10-22.
If reporting is unavailable,
contact the maintainer through an existing verified private conversation, or ask
for a private channel before sending vulnerability details. Do not
use a public issue, pull request, CI log, or an unsolicited attachment as a private
report. Access to a private repository does not make an issue confidential from
its other collaborators.

1. Share the BuildLens version, Python/OS versions, a high-level impact summary,
   and minimal synthetic reproduction steps privately. Omit real credentials,
   personal paths, private logs, and proprietary source.
2. The maintainer confirms receipt in that channel, reproduces with synthetic
   data, and coordinates a fix and disclosure privately with the reporter.
   No response deadline, bounty, or outcome is promised.
3. Share additional sensitive details only after agreeing on the private channel
   and its recipients. Redaction alone is not permission to share a private log.

The maintainer enabled PVR after the approved public visibility change. The
initial owner-account check was not considered independent verification; the
subsequent separate-account check above completed that gate. Recheck the channel
if repository access or reporting settings change. Do not submit a fake report
or advisory as a test. See
[GitHub's configuration instructions](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository).

For reports received through GitHub, the maintainer acknowledges within the
private advisory, keeps reproduction and remediation there with explicitly
agreed participants, and coordinates disclosure timing with the reporter.
Request synthetic reproductions and minimum necessary details. Never attach
real credentials or private logs, even to an advisory. No SLA or bounty is
promised. If private reporting is unavailable, use the verified private channel
described above or request one without disclosing vulnerability details.
Public issue forms remain for nonconfidential synthetic reproductions only.

## Trust boundaries

Treat logs as untrusted input. BuildLens reads regular text files with size and
line limits, never modifies them, never executes their commands, and never
contacts a network service. It strips terminal control sequences and escapes
untrusted Markdown/HTML. JSON is serialized rather than assembled by string
interpolation. Analyze stable local files; do not allow an adversary to replace
input paths during a read. POSIX files are opened nonblocking and the opened
descriptor is checked again, preventing a FIFO replacement from blocking the
normal read path. This is not a guarantee against hostile filesystems or concurrent
file mutation. Follow normal OS access controls for files and reports.

Common password/token/API-key assignments (including escaped quoted values),
CLI-style secret arguments, npm `_auth` assignments, Authorization header values,
Basic/Bearer credentials, scheme-based URL userinfo, common GitHub/AWS/Slack token
shapes, JWT-shaped tokens, and PEM
private-key blocks are masked before rules and fingerprints run. Sanitization
also applies to the displayed source name and CLI usage errors. Input error
messages deliberately avoid echoing filenames or OS exception details. Chained
OS exception details are suppressed in normal formatted reader tracebacks.
Raw exception objects still exist inside the process; this is not a memory eraser.
Bidirectional override/isolate controls are removed to reduce visual spoofing.

Masking cannot identify every secret. Unlabelled credentials, nonstandard
encodings, split or obfuscated tokens, personal information, proprietary source
snippets, sensitive paths, malformed quoting, and cookie values may remain.
Conservative masking can also remove useful context or cause UNKNOWN results.
**Review all generated reports before
sharing.** Original logs still contain their original secrets; protect and retain
them according to your organization's policy. A sanitized fingerprint can still
reveal that two known messages match; it is not a password hash.

Rules may produce false positives or miss errors. Advice is informational and
must be reviewed by a human; it is never proof of the root cause or permission
to broaden access, bypass validation, or disclose credentials.
