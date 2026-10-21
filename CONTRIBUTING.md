# Contributing

Use Python 3.11+ and a project-local virtual environment. Install `.[dev]` as
shown in README. Run pytest, Ruff lint, Ruff format checking, and a package build
before submitting changes. Never claim a check passed without running it.

Keep runtime dependencies minimal; prefer the standard library. Add narrow,
reviewable rules in `rules.py`, with cautious explanations and investigation
steps. Add synthetic positive, negative, and overlapping-signature tests. Check
line numbers, redaction, deterministic fingerprints, and all output formats.
Do not upload real private build logs, even for regression tests.

No log-derived command may execute. No automatic fixes, network calls, telemetry,
or external credentials belong in the analysis path. Report security issues
according to SECURITY.md. Discuss schema changes and broadened scope before
implementation. Contributions are under the MIT License. Submit only work you
have the right to contribute under that license. The project notice does not
assert a particular number of contributors or invent individual authorship.

Release changes also require `python tools/check_distribution.py` after building,
and `python tools/smoke_wheel.py` from an environment containing the built wheel.
The latter deliberately rejects editable source installs. Run
`python tools/evaluate.py` to reproduce the labelled synthetic diagnostic
evaluation; all 22 current synthetic cases must retain expected categories and
source line numbers. Explicit documentation-example labels are excluded from
actionable diagnoses; arbitrary quoted errors are not. This corpus is not a
general accuracy benchmark. On Linux, `sh tools/check_linux_fifo.sh` checks
real special files when unprivileged mount namespaces are available. It creates
a temporary filesystem only inside the checkout and does not install system software.

Hosted run 39667229407 passed the initial Ubuntu/Windows × Python 3.11–3.14
matrix. Source or workflow changes require a fresh matrix on the exact proposed
release commit. macOS and Ubuntu 26 remain unverified. Follow the publication
checklist; local validation does not authorize a commit, push, or public release.
