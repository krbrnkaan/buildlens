"""Run after installing a wheel; -I prevents source imports masking packaging defects."""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    scratch = root / ".tmp"
    scratch.mkdir(exist_ok=True)
    env = dict(os.environ, PYTHONNOUSERSITE="1")
    env.pop("PYTHONPATH", None)
    with tempfile.TemporaryDirectory(dir=scratch) as directory:
        installed = subprocess.run(
            [sys.executable, "-I", "-c", "import buildlens; print(buildlens.__file__)"],
            cwd=directory,
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=15,
        )
        assert installed.returncode == 0, installed.stderr
        assert not Path(installed.stdout.strip()).resolve().is_relative_to(root / "src"), (
            "Install the built wheel in this environment before running the smoke check"
        )

        def run(*args: str) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                [sys.executable, "-I", "-m", "buildlens", *args],
                cwd=directory,
                env=env,
                capture_output=True,
                text=True,
                check=False,
                timeout=15,
            )

        for format in ("terminal", "json", "markdown"):
            result = run("analyze", str(root / "samples/mixed.log"), "--format", format)
            assert result.returncode == 0, result.stderr
            if format == "json":
                report = json.loads(result.stdout)
                assert report["schema_version"] == "1.0"
                assert len(report["diagnoses"]) == 6
            else:
                assert "PYTHON_MODULE" in result.stdout
        result = run("analyze", str(root / "samples/unknown.txt"), "--format", "json")
        assert result.returncode == 1
        assert json.loads(result.stdout)["diagnoses"][0]["category"] == "UNKNOWN"
        result = run("analyze", str(Path(directory) / "missing.log"), "--format", "json")
        assert result.returncode == 2
        assert "error" in json.loads(result.stdout)
        assert run("--help").returncode == 0
        assert run("--version").stdout.strip() == "0.1.0"
    print("Installed-wheel smoke: all formats, UNKNOWN, input error, help, version passed")


if __name__ == "__main__":
    main()
