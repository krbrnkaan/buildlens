"""All test inputs are synthetic; no private build logs."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
    return subprocess.run(
        [sys.executable, "-m", "buildlens", *args],
        capture_output=True,
        text=True,
        env=env,
        check=False,
        timeout=10,
    )


def test_missing_module_cli(tmp_path: Path) -> None:
    log = tmp_path / "build.log"
    log.write_bytes(b"Starting\r\n\x1b[31mModuleNotFoundError: No module named 'demo'\x1b[0m\r\n")
    result = run_cli("analyze", str(log), "--format", "json")
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["schema_version"] == "1.0"
    assert report["diagnoses"][0]["category"] == "PYTHON_MODULE"
    assert report["diagnoses"][0]["evidence"][0]["line"] == 2


@pytest.mark.parametrize(
    ("message", "category"),
    [
        ("Could not resolve all files for configuration ':compileClasspath'.", "JVM_DEPENDENCY"),
        ("Could not find org.example:library:1.2.", "JVM_DEPENDENCY"),
        (
            "[ERROR] Could not resolve dependencies for project org.example:demo:jar:1",
            "JVM_DEPENDENCY",
        ),
        ("Could not transfer artifact org.example:demo from central", "JVM_DEPENDENCY"),
        ("npm ERR! code ERESOLVE", "NPM_DEPENDENCY"),
        ("npm error code ETARGET", "NPM_DEPENDENCY"),
        ("npm ERR! 404 No matching version found for demo@99", "NPM_DEPENDENCY"),
        ("npm error `npm ci` can only install with an existing package-lock.json", "NPM_LOCKFILE"),
        ("npm ERR! Missing: demo@1.0.0 from lock file", "NPM_LOCKFILE"),
        ("npm ci requires package.json and package-lock.json to be in sync", "NPM_LOCKFILE"),
        ("ImportError: No module named example", "PYTHON_MODULE"),
        ("OSError: [Errno 13] Permission denied: '/synthetic/path'", "PERMISSION"),
        ("npm error code EPERM", "PERMISSION"),
        ("Access is denied", "PERMISSION"),
        ("OSError: [Errno 28] No space left on device", "DISK_SPACE"),
        ("npm ERR! code ENOSPC", "DISK_SPACE"),
        ("There is not enough space on the disk", "DISK_SPACE"),
        ("fatal: Authentication failed for https://example.invalid/repo", "AUTHENTICATION"),
        ("HTTP 401 Unauthorized", "AUTHENTICATION"),
        ("Could not transfer artifact demo: status code: 403", "AUTHENTICATION"),
        ("git@example.invalid: Permission denied (publickey).", "AUTHENTICATION"),
        ("npm error code E401", "AUTHENTICATION"),
        ("Error: Unable to resolve action example/missing@v1", "GITHUB_ACTIONS"),
        ("Error: Can't find 'action.yml', 'action.yaml' or 'Dockerfile'", "GITHUB_ACTIONS"),
    ],
)
def test_rules(tmp_path: Path, message: str, category: str) -> None:
    from buildlens.analyzer import analyze

    path = tmp_path / "input.log"
    path.write_text("Starting\n" + message + "\nProcess completed with exit code 1.\n")
    report = analyze(path)
    assert [d.category for d in report.diagnoses] == [category]
    assert report.diagnoses[0].evidence[0].line == 2
    assert report.diagnoses[0].evidence[0].text == message


@pytest.mark.parametrize(
    "text",
    [
        "",
        "Build completed successfully",
        "Installing dependency tree",
        "Disk space available: 42GB",
        "No module named example is a possible exception message",
        "HTTP 200 OK",
        "Process completed with exit code 1.",
        "##[error]Process completed with exit code 127.",
        "BUILD FAILURE",
        "Error: synthetic compiler failure",
        "package.json and package-lock.json are in sync",
        "npm ci reads package-lock.json",
    ],
)
def test_unknown_and_false_positives(tmp_path: Path, text: str) -> None:
    from buildlens.analyzer import analyze

    path = tmp_path / "input.txt"
    path.write_text(text)
    report = analyze(path)
    assert report.diagnoses[0].category == "UNKNOWN"
    if "exit code" in text:
        assert report.diagnoses[0].evidence[0].line == 1


def test_duplicate_grouping_and_limits(tmp_path: Path) -> None:
    from buildlens.analyzer import analyze

    path = tmp_path / "repeat.log"
    path.write_text("ModuleNotFoundError: No module named 'demo'\n" * 7)
    first = analyze(path)
    second = analyze(path)
    assert len(first.diagnoses) == 1
    assert first.diagnoses[0].occurrences == 7
    assert len(first.diagnoses[0].evidence) == 5
    assert first.diagnoses[0].fingerprint == second.diagnoses[0].fingerprint
    path.write_text(
        "\n".join(f"ModuleNotFoundError: No module named 'package{i}'" for i in range(102))
    )
    report = analyze(path)
    assert len(report.diagnoses) == 100
    assert report.warnings


@pytest.mark.parametrize("format", ["terminal", "json", "markdown"])
def test_secrets_all_outputs(tmp_path: Path, format: str) -> None:
    path = tmp_path / "token=filename-secret.log"
    path.write_text(
        "##[error] password=hunter123 token=token123 api_key=key123 "
        "Authorization: Bearer bearer123 https://user:pass123@example.invalid "
        '"client_secret": "jsonsecret" ghp_' + "A" * 36 + "\n"
        "-----BEGIN PRIVATE KEY-----\nprivatesecret\n-----END PRIVATE KEY-----\n"
        "##[error] AWS_ACCESS_KEY_ID=AKIA1234567890123456\n"
    )
    original = path.read_bytes()
    result = run_cli("analyze", str(path), "--format", format)
    assert result.returncode == 1
    for secret in [
        "hunter123",
        "token123",
        "key123",
        "bearer123",
        "pass123",
        "jsonsecret",
        "privatesecret",
        "A" * 36,
        "filename-secret",
        "AKIA1234567890123456",
    ]:
        assert secret not in result.stdout
        assert secret not in result.stderr
    assert "REDACTED" in result.stdout
    assert path.read_bytes() == original


def test_redaction_line_numbers_and_controls(tmp_path: Path) -> None:
    from buildlens.analyzer import analyze

    path = tmp_path / "controls.log"
    path.write_bytes(
        b"-----BEGIN PRIVATE KEY-----\r\nsecret\r\n-----END PRIVATE KEY-----\r\n"
        b"\x1b]8;;https://example.invalid\x07ModuleNotFoundError: No module named 'x'"
        b"\x1b]8;;\x1b\\\x08\r\n"
    )
    evidence = analyze(path).diagnoses[0].evidence[0]
    assert evidence.line == 4
    assert "\x1b" not in evidence.text and "\x08" not in evidence.text


@pytest.mark.parametrize(
    "data",
    [
        b"hello\xff\nModuleNotFoundError: No module named 'demo'",
        "hello\nModuleNotFoundError: No module named 'demo'".encode("utf-16"),
        b"\xef\xbb\xbfhello\rModuleNotFoundError: No module named 'demo'",
    ],
)
def test_encoding(tmp_path: Path, data: bytes) -> None:
    from buildlens.analyzer import analyze

    path = tmp_path / "encoding.LOG"
    path.write_bytes(data)
    report = analyze(path)
    assert report.diagnoses[0].evidence[0].line == 2
    assert bool(report.warnings) == (b"\xff\n" in data)


@pytest.mark.parametrize("kind", ["missing", "extension", "directory", "size", "line", "lines"])
def test_rejects_bad_input(tmp_path: Path, kind: str) -> None:
    path = tmp_path / "input.log"
    if kind == "extension":
        path = tmp_path / "input.bin"
        path.write_bytes(b"error")
    elif kind == "directory":
        path.mkdir()
    elif kind == "size":
        with path.open("wb") as stream:
            stream.truncate(10 * 1024 * 1024 + 1)
    elif kind == "line":
        path.write_text("x" * 16_385)
    elif kind == "lines":
        path.write_text("x\n" * 100_001)
    result = run_cli("analyze", str(path), "--format", "json")
    assert result.returncode == 2
    assert "error" in json.loads(result.stdout)
    assert "Traceback" not in result.stderr


def test_markdown_does_not_render_untrusted_html(tmp_path: Path) -> None:
    path = tmp_path / "markup.log"
    path.write_text("##[error]<script>alert(1)</script> [run](https://example.invalid) `cmd`")
    result = run_cli("analyze", str(path), "--format", "markdown")
    assert "<script>" not in result.stdout
    assert "[run](" not in result.stdout
    assert "\\`cmd\\`" in result.stdout


def test_cli_usage_and_terminal(tmp_path: Path) -> None:
    assert run_cli().returncode == 2
    assert run_cli("--help").returncode == 0
    assert run_cli("--version").stdout.strip() == "0.1.0"
    path = tmp_path / "example.txt"
    path.write_text("No space left on device")
    result = run_cli("analyze", str(path))
    assert result.returncode == 0
    assert "DISK_SPACE" in result.stdout and "L1:" in result.stdout
    assert "Next step:" in result.stdout
    assert run_cli("analyze", str(path), "--format", "xml").returncode == 2


def test_untrusted_commands_never_execute(tmp_path: Path) -> None:
    marker = tmp_path / "must-not-exist"
    path = tmp_path / "commands.log"
    path.write_text(f'##[error] run: touch "{marker}"\n$(echo synthetic)\n')
    assert run_cli("analyze", str(path)).returncode == 1
    assert not marker.exists()


def test_usage_errors_redact_secrets() -> None:
    result = run_cli("analyze", "input.log", "--format", "token=synthetic-secret")
    assert result.returncode == 2
    assert "synthetic-secret" not in result.stderr


def test_long_evidence_keeps_the_matching_error(tmp_path: Path) -> None:
    from buildlens.analyzer import analyze

    path = tmp_path / "long.log"
    path.write_text("prefix " * 300 + "ModuleNotFoundError: No module named 'demo'")
    evidence = analyze(path).diagnoses[0].evidence[0]
    assert "ModuleNotFoundError" in evidence.text
    assert len(evidence.text) <= 1000


def test_unknown_counts_all_generic_occurrences(tmp_path: Path) -> None:
    from buildlens.analyzer import analyze

    path = tmp_path / "unknown.txt"
    path.write_text("##[error]unrecognized failure\n" * 9)
    diagnosis = analyze(path).diagnoses[0]
    assert diagnosis.occurrences == 9
    assert len(diagnosis.evidence) == 5


def test_fingerprint_normalization() -> None:
    from buildlens.analyzer import fingerprint

    assert fingerprint("x", "2026-10-21T12:30:01Z ERROR: demo") == fingerprint("x", "error:  demo")
    assert fingerprint("x", "error: demo") != fingerprint("x", "error: other")
    assert fingerprint("x", "error: demo") != fingerprint("y", "error: demo")


def test_read_error_does_not_leak_os_details(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from buildlens.reader import InputError, read_log

    path = tmp_path / "file.log"
    path.touch()

    def denied(*args: object, **kwargs: object) -> None:
        raise PermissionError("password=synthetic-sensitive")

    monkeypatch.setattr(os, "open", denied)
    with pytest.raises(InputError, match="Cannot read input file") as error:
        read_log(path)
    assert "synthetic-sensitive" not in str(error.value)


def test_samples_are_analyzable() -> None:
    from buildlens.analyzer import analyze

    for path in (ROOT / "samples").iterdir():
        if path.suffix not in {".log", ".txt"}:
            continue
        report = analyze(path)
        assert bool(report.diagnoses)
        assert (report.diagnoses[0].category == "UNKNOWN") == (path.name == "unknown.txt")


def test_multiline_terminal_sequence_preserves_line_numbers(tmp_path: Path) -> None:
    from buildlens.analyzer import analyze

    path = tmp_path / "osc.log"
    path.write_bytes(b"\x1b]0;title\ncontinued\x07\nModuleNotFoundError: No module named 'demo'")
    report = analyze(path)
    assert report.lines == 3
    assert report.diagnoses[0].evidence[0].line == 3


def test_redaction_does_not_join_physical_lines(tmp_path: Path) -> None:
    from buildlens.analyzer import analyze

    path = tmp_path / "redaction.log"
    path.write_text("token=\nBearer\nModuleNotFoundError: No module named 'demo'")
    report = analyze(path)
    assert report.lines == 3
    assert report.diagnoses[0].category == "PYTHON_MODULE"
    assert report.diagnoses[0].evidence[0].line == 3


def test_long_neutral_identifier_does_not_stall_cli(tmp_path: Path) -> None:
    path = tmp_path / "neutral.log"
    path.write_text("x" * 16_384 + "\nNo space left on device")
    result = run_cli("analyze", str(path), "--format", "json")
    assert result.returncode == 0
    assert json.loads(result.stdout)["diagnoses"][0]["evidence"][0]["line"] == 2
