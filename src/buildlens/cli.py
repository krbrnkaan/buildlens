"""CLI contract: 0 analyzed, 1 unknown, 2 input/usage error."""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import TextIO

from buildlens import __version__
from buildlens.analyzer import analyze
from buildlens.reader import InputError
from buildlens.redaction import redact
from buildlens.render import render


class SafeParser(argparse.ArgumentParser):
    def _print_message(self, message: str | None, file: TextIO | None = None) -> None:
        if message:
            super()._print_message(redact(message), file)


def main(argv: list[str] | None = None) -> int:
    parser = SafeParser(prog="buildlens", description="Offline CI/build log diagnosis")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    command = commands.add_parser("analyze", help="Analyze a .log or .txt file")
    command.add_argument("logfile", type=Path)
    command.add_argument("--format", choices=("terminal", "json", "markdown"), default="terminal")
    args = parser.parse_args(argv)
    try:
        report = analyze(args.logfile)
    except InputError as exc:
        if args.format == "json":
            output = json.dumps({"schema_version": "1.0", "error": str(exc)})
            stream = sys.stdout
        else:
            output = f"buildlens: {exc}"
            stream = sys.stderr
        status = 2
    else:
        output = render(report, args.format)
        stream = sys.stdout
        status = 1 if report.diagnoses[0].category == "UNKNOWN" else 0
    try:
        # Console encodings vary on Windows; reports must remain printable.
        encoding = stream.encoding or "utf-8"
        print(
            output.encode(encoding, errors="backslashreplace").decode(encoding),
            file=stream,
            flush=True,
        )
    except OSError:
        # Prevent a second failed buffer flush at interpreter shutdown (exit 120).
        try:
            with open(os.devnull, "w") as sink:
                os.dup2(sink.fileno(), stream.fileno())
        except (OSError, ValueError):
            pass
        return 2
    return status
