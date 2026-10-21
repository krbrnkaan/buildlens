"""Explicit signatures, not an inferred root-cause model."""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    id: str
    category: str
    pattern: re.Pattern[str]
    explanation: str
    next_step: str


def rule(id: str, category: str, pattern: str, explanation: str, next_step: str) -> Rule:
    return Rule(id, category, re.compile(pattern, re.I), explanation, next_step)


RULES = (
    rule(
        "disk-space",
        "DISK_SPACE",
        r"\b(?:no space left on device|ENOSPC|disk full|"
        r"not enough space on (?:the )?disk)\b",
        "The log reports exhausted storage or a storage quota; "
        "the affected resource is unverified.",
        "Check free space, inode availability, and quotas on the failing runner.",
    ),
    rule(
        "credentials",
        "AUTHENTICATION",
        r"\b(?:authentication failed|bad credentials|"
        r"invalid (?:authentication|access|api|bearer) token|unable to authenticate|E401|E403|"
        r"permission denied \(publickey\)|401 unauthorized|403 forbidden|"
        r"status code[: ]+(?:401|403)|could not read Username)(?!\w)",
        "The request appears to have been rejected for credentials or access rights.",
        "Verify credential availability, expiry, scope, and repository or registry access; "
        "do not print credentials.",
    ),
    rule(
        "permission",
        "PERMISSION",
        r"\b(?:permission denied|EACCES|EPERM|access is denied)\b",
        "The operation reports denied access; ownership, policy, or a file lock may be involved.",
        "Check the runner identity and permissions for the affected path or operation; "
        "avoid granting blanket administrator access.",
    ),
    rule(
        "python-module",
        "PYTHON_MODULE",
        r"\b(?:ModuleNotFoundError|ImportError):\s*No module named\b",
        "Python could not import a module in the active environment; "
        "the package or path may be missing.",
        "Check the interpreter, virtual environment, declared dependencies, "
        "and module search path.",
    ),
    rule(
        "npm-lockfile",
        "NPM_LOCKFILE",
        r"(?:npm (?:ERR!|error).*\bELOCKVERIFY\b|"
        r"npm ci.*(?:requires|can only install|cannot|must).*(?:package-lock|lockfile)|"
        r"(?:package\.json|package-lock\.json).*\b(?:out of sync|to be in sync)\b|"
        r"npm (?:ERR!|error).*Missing: .* from lock file)",
        "npm reports a lockfile or clean-install precondition problem; "
        "inspect the paired error lines.",
        "Compare package.json with the committed lockfile and npm version; regenerate and review "
        "the lockfile in a trusted development environment if needed.",
    ),
    rule(
        "npm-dependency",
        "NPM_DEPENDENCY",
        r"npm (?:ERR!|error).*\b(?:ERESOLVE|ETARGET|E404)\b|"
        r"\bunable to resolve dependency tree\b|"
        r"npm (?:ERR!|error).*\bNo matching version found for\b",
        "npm reports a dependency resolution or package availability problem.",
        "Check package versions, peer dependency constraints, and the configured registry.",
    ),
    rule(
        "jvm-dependency",
        "JVM_DEPENDENCY",
        r"\b(?:Could not resolve all (?:files|dependencies)|"
        r"Could not (?:find|resolve) [\w.-]+:[\w.-]+:[\w.+-]+|"
        r"Could not resolve dependencies for project|Could not transfer artifact|"
        r"Could not find artifact|Failed to collect dependencies)\b",
        "Gradle or Maven reports an artifact resolution failure; availability, network, "
        "configuration, or access may be involved.",
        "Check artifact coordinates, repository configuration, connectivity, and any more specific "
        "authentication error in the report.",
    ),
    rule(
        "github-action",
        "GITHUB_ACTIONS",
        r"(?:\bUnable to resolve action\b|"
        r"Can't find 'action\.ya?ml'|\bUnable to download action\b)",
        "The workflow reports an action resolution or metadata failure.",
        "Check the action owner, repository, pinned ref, metadata path, and runner access.",
    ),
)

# Only an explicit line label establishes example context; quotation alone does not.
DOCUMENTATION_EXAMPLE = re.compile(r"^\s*Documentation example:\s*", re.I)

GENERIC = re.compile(
    r"(?:##\[error\]|\bProcess completed with exit code [1-9]\d*|"
    r"\bexit (?:code|status)[: ]+[1-9]\d*|\bBUILD (?:FAILED|FAILURE)\b|"
    r"\b[A-Za-z_]\w*(?:Error|Exception):|"
    r"\b(?:Error|Exception|FAILED|fatal)\b)",
    re.I,
)
