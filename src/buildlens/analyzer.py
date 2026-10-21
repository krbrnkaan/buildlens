"""Evidence collection and stable, explainable duplicate grouping."""

import hashlib
import re
from pathlib import Path

from buildlens.models import Diagnosis, Evidence, Report
from buildlens.reader import read_log
from buildlens.redaction import redact
from buildlens.rules import DOCUMENTATION_EXAMPLE, GENERIC, RULES

MAX_GROUPS = 100
MAX_EVIDENCE = 5
MAX_EVIDENCE_CHARS = 1000


def excerpt(line: str, match: re.Match[str]) -> str:
    offset = max(0, match.start() - 100, match.end() - (MAX_EVIDENCE_CHARS - 4))
    prefix = "... " if offset else ""
    return prefix + line[offset : offset + MAX_EVIDENCE_CHARS - len(prefix)]


def fingerprint(rule_id: str, text: str) -> str:
    normalized = " ".join(text.casefold().split())
    normalized = re.sub(r"^\d{4}-\d\d-\d\d[t ][\d:.+z-]+\s*", "", normalized)
    return hashlib.sha256(f"{rule_id}\n{normalized}".encode()).hexdigest()[:16]


def analyze(path: Path) -> Report:
    text, warnings = read_log(path)
    lines = redact(text).split("\n") if text else []
    if lines and lines[-1] == "":
        lines.pop()
    groups: dict[str, Diagnosis] = {}
    generic: list[Evidence] = []
    generic_count = 0
    omitted = False
    for number, line in enumerate(lines, 1):
        example = DOCUMENTATION_EXAMPLE.match(line)
        matched = (
            None if example else next((rule for rule in RULES if rule.pattern.search(line)), None)
        )
        if matched is None:
            if generic_match := example or GENERIC.search(line):
                generic_count += 1
                if len(generic) < MAX_EVIDENCE:
                    generic.append(Evidence(number, excerpt(line, generic_match)))
            continue
        key = fingerprint(matched.id, line)
        if key not in groups:
            if len(groups) >= MAX_GROUPS:
                omitted = True
                continue
            groups[key] = Diagnosis(
                matched.category,
                matched.id,
                key,
                matched.explanation,
                matched.next_step,
            )
        diagnosis = groups[key]
        diagnosis.occurrences += 1
        if len(diagnosis.evidence) < MAX_EVIDENCE:
            match = matched.pattern.search(line)
            assert match is not None
            diagnosis.evidence.append(Evidence(number, excerpt(line, match)))
    if omitted:
        warnings.append("Additional distinct diagnoses omitted after the 100-group limit.")
    diagnoses = list(groups.values())
    if not diagnoses:
        diagnoses.append(
            Diagnosis(
                "UNKNOWN",
                "unknown",
                fingerprint("unknown", ""),
                "Insufficient recognized evidence to explain this log. "
                "This does not establish success.",
                "Inspect the failing step and preceding output; "
                "capture a more detailed log if needed.",
                generic_count,
                generic,
            )
        )
    return Report(
        redact(path.name).replace("\n", " ").replace("\r", " "), len(lines), diagnoses, warnings
    )
