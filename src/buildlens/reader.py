"""Bounded reads of regular text files, without modifying the source."""

import codecs
import os
import stat
from pathlib import Path

MAX_BYTES = 10 * 1024 * 1024
MAX_LINES = 100_000
MAX_LINE_LENGTH = 16_384


class InputError(ValueError):
    """An unsupported, unavailable, or oversized input."""


def read_log(path: Path) -> tuple[str, list[str]]:
    if path.suffix.lower() not in {".log", ".txt"}:
        raise InputError("Input must have a .log or .txt extension.")
    try:
        if not stat.S_ISREG(path.stat().st_mode):
            raise InputError("Input must be a regular file.")
        flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_BINARY", 0)
        with os.fdopen(os.open(path, flags), "rb") as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                raise InputError("Input must be a regular file.")
            data = stream.read(MAX_BYTES + 1)
    except OSError:
        raise InputError("Cannot read input file; check its existence and permissions.") from None
    if len(data) > MAX_BYTES:
        raise InputError("Input exceeds the 10 MiB limit; split it into smaller log files.")
    encoding = (
        "utf-16" if data.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)) else "utf-8-sig"
    )
    text = data.decode(encoding, errors="replace").replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    if len(lines) - int(text.endswith("\n")) > MAX_LINES:
        raise InputError("Input exceeds the 100,000 line limit.")
    if any(len(line) > MAX_LINE_LENGTH for line in lines):
        raise InputError("Input contains a line longer than 16,384 characters.")
    warnings = (
        ["Invalid text encoding was replaced; evidence may be incomplete."]
        if "\ufffd" in text
        else []
    )
    return text, warnings
