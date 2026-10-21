# BuildLens engineering rules

- Work only within this repository. Do not inspect or reuse other local projects.
- Keep Python 3.11+ compatibility and the src layout. Prefer standard-library runtime code.
- No LLM calls, API keys, telemetry, paid services, network analysis, or log command execution.
- Use synthetic fixtures only. Never add private project logs or credentials.
- Preserve original physical line numbers and sanitize every output boundary.
- Unsupported evidence must yield UNKNOWN. Explain symptoms cautiously.
- Keep changes small; add meaningful positive and false-positive regression cases.
- Run `python -m pytest -q`, `python -m ruff check .`, and
  `python -m ruff format --check .` using the local virtual environment.
- Verify packaging when changing metadata or entry points. Report actual results and limitations.
- Do not publish, push, deploy, create remotes, or install global software without approval.
- Use context-mode processing tools for large or analytical command output when available.
