"""Versioned, serializable report data."""

from dataclasses import dataclass, field


@dataclass
class Evidence:
    line: int
    text: str


@dataclass
class Diagnosis:
    category: str
    rule_id: str
    fingerprint: str
    explanation: str
    next_step: str
    occurrences: int = 0
    evidence: list[Evidence] = field(default_factory=list)


@dataclass
class Report:
    source: str
    lines: int
    diagnoses: list[Diagnosis]
    warnings: list[str]
    schema_version: str = "1.0"
