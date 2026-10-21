# Security policy

BuildLens 0.1.x is an early CLI. No hosted security reporting channel or remote
repository has been configured in this preparation. No contact email is specified.
There is no guaranteed response time or formal security support commitment.

## Confidential disclosure

During local/private CI evaluation, contact the maintainer through the existing,
verified private conversation in which you obtained access. If you have no such
channel, ask the maintainer for one before sending vulnerability details. Do not
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

When the repository becomes public, the maintainer **must enable GitHub Private
Vulnerability Reporting**, verify that Security → Report a vulnerability is
available, and document the actual reporting destination before announcing the
release. This feature is for public repositories; its availability is not claimed
during private evaluation. See [GitHub's configuration instructions](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository).
Enabling it or changing visibility requires separate maintainer approval. Public
issue forms remain for nonconfidential synthetic reproductions only.

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
