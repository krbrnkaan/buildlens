"""Reproduce a labelled synthetic evaluation, not a real-world accuracy benchmark."""

import json
import tempfile
from dataclasses import asdict
from pathlib import Path

from buildlens.analyzer import analyze
from buildlens.redaction import redact


def evaluate() -> dict[str, object]:
    root = Path(__file__).resolve().parents[1]
    cases = json.loads((root / "samples/evaluation.json").read_text(encoding="utf-8"))
    scratch = root / ".tmp"
    scratch.mkdir(exist_ok=True)
    results = []
    with tempfile.TemporaryDirectory(dir=scratch) as directory:
        for case in cases:
            path = Path(directory) / (case["id"] + ".log")
            path.write_text(case["log"], encoding="utf-8")
            report = analyze(path)
            categories = list(dict.fromkeys(d.category for d in report.diagnoses))
            evidence = [e for d in report.diagnoses for e in d.evidence]
            lines = sorted(e.line for e in evidence)
            original = redact(case["log"]).splitlines()
            grounded = all(
                1 <= e.line <= len(original) and e.text.removeprefix("... ") in original[e.line - 1]
                for e in evidence
            )
            assert grounded, case["id"]
            assert path.read_text(encoding="utf-8") == case["log"]
            results.append(
                {
                    "id": case["id"],
                    "expected_categories": case["categories"],
                    "actual_categories": categories,
                    "category_agreement": categories == case["categories"],
                    "line_agreement": lines == case["evidence_lines"],
                    "evidence_grounded": grounded,
                    "advice_present": all(d.explanation and d.next_step for d in report.diagnoses),
                    "occurrences": [d.occurrences for d in report.diagnoses],
                }
            )
            if case["id"] == "credential-and-permission":
                assert "synthetic-evaluation-password" not in json.dumps(asdict(report))
    return {"corpus": "synthetic-v1", "cases": len(results), "results": results}


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
