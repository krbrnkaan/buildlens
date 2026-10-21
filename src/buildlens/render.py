"""Render only sanitized report data; never embed active log markup."""

import html
import json
from dataclasses import asdict

from buildlens.models import Report


def markdown_text(text: str) -> str:
    text = html.escape(text, quote=False)
    for char in "\\`*_{}[]()#+-.!|>~":
        text = text.replace(char, "\\" + char)
    return text


def render(report: Report, format: str) -> str:
    if format == "json":
        return json.dumps(asdict(report), indent=2, ensure_ascii=True)
    md = format == "markdown"
    escape = markdown_text if md else str
    output = [f"{'# ' if md else ''}BuildLens: {escape(report.source)}", f"Lines: {report.lines}"]
    output.extend(f"Warning: {escape(warning)}" for warning in report.warnings)
    for diagnosis in report.diagnoses:
        output.extend(
            [
                "",
                f"{'## ' if md else ''}{diagnosis.category} ({diagnosis.rule_id})",
                f"Fingerprint: {diagnosis.fingerprint}; occurrences: {diagnosis.occurrences}",
                escape(diagnosis.explanation),
                f"Next step: {escape(diagnosis.next_step)}",
            ]
        )
        output.extend(f"- L{item.line}: {escape(item.text)}" for item in diagnosis.evidence)
    return "\n".join(output)
