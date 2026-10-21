"""Best-effort secret masking and removal of terminal control sequences."""

import re

ANSI = re.compile(r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)|\x1b\[[0-?]*[ -/]*[@-~]")
CONTROL = re.compile(r"[\x00-\x08\x0b-\x1f\x7f-\x9f\u202a-\u202e\u2066-\u2069]")
VALUE = r"""(?:"(?:\\[^\r\n]|[^"\\\r\n])*"|'(?:\\[^\r\n]|[^'\\\r\n])*'|[^\s,;]+)"""
SENSITIVE = r"(?:password|passwd|secret|token|api[_-]?key|access[_-]?key|_auth)"
ASSIGNMENT = re.compile(
    rf"""(?ix)(?<![\w-])(["']?(?=[\w-]*{SENSITIVE})
    [\w-]+["']?[ \t]*[:=][ \t]*){VALUE}"""
)
CLI_SECRET = re.compile(rf"(?i)(?<![\w-])(--?(?=[\w-]*{SENSITIVE})[\w-]+[ \t]+){VALUE}")
AUTH_HEADER = re.compile(r"(?im)(\b(?:proxy-)?authorization[ \t]*:[ \t]*)[^\r\n]+")
AUTH = re.compile(r"(?i)\b(Bearer|Basic)[ \t]+[A-Za-z0-9._~+/=-]+")
URL_AUTH = re.compile(r"(?<![\w+.-])([a-z][a-z0-9+.-]*://)[^\s/@]+@", re.I)
KNOWN = re.compile(
    r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
    r"(?:AKIA|ASIA)[A-Z0-9]{16}|xox[baprs]-[A-Za-z0-9-]+|"
    r"(?<![A-Za-z0-9_-])eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)\b"
)
PRIVATE_KEY = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?(?:-----END [A-Z ]*PRIVATE KEY-----|\Z)",
    re.S,
)


def redact(text: str) -> str:
    text = ANSI.sub(lambda m: "\n" * m[0].count("\n"), text)
    # Preserve line structure so evidence still points into the original log.
    text = PRIVATE_KEY.sub(lambda m: "[REDACTED]" + "\n" * m[0].count("\n"), text)
    text = CONTROL.sub("", text)
    text = URL_AUTH.sub(r"\1[REDACTED]@", text)
    text = ASSIGNMENT.sub(r"\1[REDACTED]", text)
    text = CLI_SECRET.sub(r"\1[REDACTED]", text)
    text = AUTH_HEADER.sub(r"\1[REDACTED]", text)
    text = AUTH.sub(r"\1 [REDACTED]", text)
    return KNOWN.sub("[REDACTED]", text)
