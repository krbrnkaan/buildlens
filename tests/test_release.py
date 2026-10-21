"""Release checks use local synthetic files and never invoke log instructions."""

import errno
import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest
from test_buildlens import ROOT, run_cli

from buildlens import __version__
from buildlens.analyzer import analyze
from buildlens.reader import InputError, read_log


def test_release_version_is_consistent() -> None:
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert metadata["project"]["version"] == __version__ == "0.1.0"
    assert metadata["project"]["requires-python"] == ">=3.11"
    assert metadata["project"]["dependencies"] == []


@pytest.mark.parametrize("name", ["space in name.log", "unicode-日志.txt", "-option-like.log"])
def test_relative_paths_are_literal_arguments(tmp_path: Path, name: str) -> None:
    path = tmp_path / name
    path.write_text("No space left on device", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "buildlens", "analyze", "--format", "json", "--", name],
        cwd=tmp_path,
        env=dict(os.environ, PYTHONPATH=str(ROOT / "src")),
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["source"] == name
    assert report["diagnoses"][0]["evidence"][0]["line"] == 1


@pytest.mark.parametrize("kind", ["regular", "broken", "loop"])
def test_symlink_inputs_are_bounded(tmp_path: Path, kind: str) -> None:
    target = tmp_path / "target.log"
    alias = tmp_path / "alias.log"
    if kind == "regular":
        target.write_text("No space left on device", encoding="utf-8")
    try:
        alias.symlink_to(alias if kind == "loop" else target)
    except (OSError, NotImplementedError):
        pytest.skip("Symlink creation unavailable in this environment")
    result = run_cli("analyze", str(alias), "--format", "json")
    assert result.returncode == (0 if kind == "regular" else 2)
    report = json.loads(result.stdout)
    if kind == "regular":
        assert report["source"] == "alias.log"
    else:
        assert "error" in report and "Traceback" not in result.stderr


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="POSIX FIFO inputs")
@pytest.mark.parametrize("symlink", [False, True])
def test_fifo_input_does_not_hang(tmp_path: Path, symlink: bool) -> None:
    fifo = tmp_path / "special.log"
    try:
        os.mkfifo(fifo)
    except OSError as exc:
        if exc.errno in {errno.ENOTSUP, errno.EOPNOTSUPP}:
            pytest.skip("Workspace filesystem does not support FIFOs")
        raise
    path = fifo
    if symlink:
        path = tmp_path / "alias.log"
        path.symlink_to(fifo)
    result = run_cli("analyze", str(path), "--format", "json")
    assert result.returncode == 2
    assert "regular file" in json.loads(result.stdout)["error"]


def test_exact_byte_limit_and_sentinel(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from buildlens import reader

    path = tmp_path / "boundary.log"
    monkeypatch.setattr(reader, "MAX_BYTES", 64)
    path.write_bytes(b"x" * 64)
    assert read_log(path)[0] == "x" * 64
    path.write_bytes(b"x" * 65)
    with pytest.raises(InputError, match="limit"):
        read_log(path)


def test_unknown_import_error_retains_actual_evidence(tmp_path: Path) -> None:
    path = tmp_path / "import.log"
    message = "ImportError: cannot import name 'synthetic' from 'example'"
    path.write_text("Starting\n" + message, encoding="utf-8")
    diagnosis = analyze(path).diagnoses[0]
    assert diagnosis.category == "UNKNOWN"
    assert [(e.line, e.text) for e in diagnosis.evidence] == [(2, message)]


def test_documentation_example_is_unknown_with_original_evidence(tmp_path: Path) -> None:
    path = tmp_path / "documentation.log"
    example = "Documentation example: No space left on device"
    path.write_text("Starting\n" + example, encoding="utf-8")
    diagnosis = analyze(path).diagnoses[0]
    assert diagnosis.category == "UNKNOWN"
    assert [(e.line, e.text) for e in diagnosis.evidence] == [(2, example)]


def test_documentation_example_does_not_hide_following_failure(tmp_path: Path) -> None:
    path = tmp_path / "mixed.log"
    path.write_text(
        "  documentation EXAMPLE: No space left on device\n"
        "ModuleNotFoundError: No module named 'synthetic'\n",
        encoding="utf-8",
    )
    diagnosis = analyze(path).diagnoses[0]
    assert diagnosis.category == "PYTHON_MODULE"
    assert [e.line for e in diagnosis.evidence] == [2]


@pytest.mark.parametrize(
    "message",
    [
        'OSError: [Errno 28] "No space left on device"',
        "Documentation build failed: No space left on device",
        "Error while copying Documentation example: No space left on device",
    ],
)
def test_operational_errors_still_match_with_quotes_or_documentation_text(
    tmp_path: Path, message: str
) -> None:
    path = tmp_path / "operational.log"
    path.write_text(message, encoding="utf-8")
    diagnosis = analyze(path).diagnoses[0]
    assert diagnosis.category == "DISK_SPACE"
    assert [(e.line, e.text) for e in diagnosis.evidence] == [(1, message)]


def test_recorded_diagnostic_evaluation_is_reproducible() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools/evaluate.py")],
        env=dict(os.environ, PYTHONPATH=str(ROOT / "src")),
        capture_output=True,
        text=True,
        check=False,
        timeout=15,
    )
    assert result.returncode == 0, result.stderr
    recorded = json.loads((ROOT / "docs/diagnostic-evaluation.json").read_text(encoding="utf-8"))
    assert json.loads(result.stdout) == recorded
    assert all(
        case["category_agreement"] and case["line_agreement"] for case in recorded["results"]
    )
