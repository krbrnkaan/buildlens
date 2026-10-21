# JSON report contract 1.0

`--format json` writes exactly one JSON object, followed by a newline. Strings
are JSON escaped. Consumers should ignore additional fields within a major schema
version and treat category/rule identifiers as extensible strings. Breaking field
changes require a new major schema version. Fingerprint normalization changes
also require a new major schema version.
The machine-readable schema is [report.schema.json](report.schema.json). Field
shapes and the fingerprint algorithm remain unchanged through milestone 1.6. Security
fixes can change sanitized text and therefore fingerprints for newly redacted
inputs. Rule fixes may change classifications; compare fingerprints only when
the rule ID and sanitized message are the same.

Generic Python exception lines can appear as UNKNOWN evidence without creating
a diagnosis of a missing module or another unverified cause.

Successful analysis has these required fields:

| Field | Type | Meaning |
| --- | --- | --- |
| schema_version | string | Exactly `1.0` |
| source | string | Redacted input basename; no absolute path |
| lines | integer >= 0 | Number of physical lines after newline normalization |
| warnings | array of strings | Encoding issues or omitted diagnosis groups |
| diagnoses | nonempty array of objects | Supported diagnoses, or a single UNKNOWN |

Each diagnosis contains:

| Field | Type | Meaning |
| --- | --- | --- |
| category | string | Category listed in README |
| rule_id | string | Stable signature identifier, or `unknown` |
| fingerprint | string | 16 lowercase hexadecimal characters; algorithm in README |
| explanation | string | Cautious description of the reported symptom |
| next_step | string | Suggested investigation, never an instruction executed by BuildLens |
| occurrences | integer >= 0 | Matched lines in this group; UNKNOWN counts generic evidence lines |
| evidence | array of objects | Up to five sanitized excerpts in original order |

An evidence object contains `line` (integer >= 1, original physical line number)
and `text` (string, sanitized excerpt, at most 1,000 characters, including an
optional `... ` prefix when leading text was omitted). Excerpts are not
byte-for-byte copies because of decoding, control stripping, redaction, and
length limits. The original file remains untouched. UNKNOWN may have no evidence.

Example (synthetic):

```json
{
  "schema_version": "1.0",
  "source": "build.log",
  "lines": 1,
  "warnings": [],
  "diagnoses": [{
    "category": "UNKNOWN",
    "rule_id": "unknown",
    "fingerprint": "0000000000000000",
    "explanation": "Insufficient recognized evidence.",
    "next_step": "Inspect preceding output.",
    "occurrences": 1,
    "evidence": [{"line": 1, "text": "Process completed with exit code 1."}]
  }]
}
```

The example fingerprint is illustrative. An input error produces only
`{"schema_version": "1.0", "error": "human-readable message"}` and exit code 2.
CLI syntax errors instead use a stderr usage message. No report is emitted for
syntax errors. A recognized diagnosis exits 0; UNKNOWN exits 1.
