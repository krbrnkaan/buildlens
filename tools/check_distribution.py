"""Assert metadata and archive contents for the locally built v0.1.0 artifacts."""

import configparser
import tarfile
import tomllib
import zipfile
from email.parser import BytesParser
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    assert project["version"] == "0.1.0"
    stem = "buildlens-0.1.0"
    required = [
        "README.md",
        "LICENSE",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "docs/report.schema.json",
        "docs/milestone-1.6-report.md",
        "samples/evaluation.json",
        "tools/evaluate.py",
        "tools/check_linux_fifo.sh",
        ".github/workflows/ci.yml",
        ".github/ISSUE_TEMPLATE/bug_report.yml",
        "docs/releases/v0.1.0.md",
    ]
    with zipfile.ZipFile(root / "dist" / f"{stem}-py3-none-any.whl") as wheel:
        metadata = BytesParser().parsebytes(wheel.read(f"{stem}.dist-info/METADATA"))
        assert metadata["Name"] == "buildlens" and metadata["Version"] == "0.1.0"
        assert metadata["Requires-Python"] == ">=3.11"
        assert metadata["License-Expression"] == "MIT"
        assert all('extra == "dev"' in value for value in metadata.get_all("Requires-Dist", []))
        entries = configparser.ConfigParser()
        entries.read_string(wheel.read(f"{stem}.dist-info/entry_points.txt").decode())
        assert entries["console_scripts"]["buildlens"] == "buildlens.cli:main"
        for source in (root / "src/buildlens").glob("*.py"):
            assert wheel.read("buildlens/" + source.name) == source.read_bytes(), source.name
        assert wheel.read(f"{stem}.dist-info/licenses/LICENSE") == (root / "LICENSE").read_bytes()
    with tarfile.open(root / "dist" / f"{stem}.tar.gz") as archive:
        for path in required:
            item = archive.extractfile(f"{stem}/{path}")
            assert item is not None and item.read() == (root / path).read_bytes(), path
        for member in archive.getmembers():
            parts = Path(member.name).parts
            assert not member.name.startswith("/") and ".." not in parts
            assert not member.issym() and not member.islnk()
            assert not any(
                p.startswith((".venv", ".tmp", ".test-tmp", "__pycache__")) for p in parts
            )
        metadata_file = archive.extractfile(f"{stem}/PKG-INFO")
        assert metadata_file is not None
        source_metadata = BytesParser().parsebytes(metadata_file.read())
        for key in ("Name", "Version", "Requires-Python", "License-Expression"):
            assert source_metadata[key] == metadata[key]
    print("Distribution metadata, entry point, license, source bytes, and archive contents passed")


if __name__ == "__main__":
    main()
