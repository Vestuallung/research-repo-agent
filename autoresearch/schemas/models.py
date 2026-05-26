from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


SCHEMA_VERSION = "autoresearch.v0"

ARTIFACT_TYPES = {
    "research_brief",
    "paper_candidate",
    "paper_audit",
    "paper_priority_list",
    "selected_experiments",
    "experiment_task",
    "experiment_log",
    "review_record",
}

STATUSES = {
    "draft",
    "candidate",
    "audited",
    "selected",
    "planned",
    "completed",
    "failed",
    "blocked",
    "needs_review",
    "checked",
}

FAILURE_TYPES = {
    "not_run",
    "missing_repo",
    "missing_dependency_manifest",
    "missing_entrypoint",
    "install_failed",
    "command_failed",
    "timeout",
    "data_missing",
    "environment_incompatible",
    "unsafe_command",
    "unknown",
}


@dataclass
class ArtifactEnvelope:
    schema_version: str
    artifact_type: str
    artifact_id: str
    created_at: str
    updated_at: str
    producer: str
    status: str
    data: dict[str, Any]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ResearchBrief:
    topic: str
    goal: str
    keywords: list[str] = field(default_factory=list)
    exclusions: list[str] = field(default_factory=list)
    questions: list[str] = field(default_factory=list)
    success_criteria: list[str] = field(default_factory=list)
    status: str = "draft"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PaperCandidate:
    paper_id: str
    title: str
    url: str
    authors: list[str] = field(default_factory=list)
    year: str = ""
    source: str = ""
    code_url: str = ""
    method_type: str = "unknown"
    relevance: int = 3
    tags: list[str] = field(default_factory=list)
    screening_reason: str = ""
    status: str = "candidate"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PaperAudit:
    paper_id: str
    title: str
    main_claims: list[str] = field(default_factory=list)
    evidence_quality: int = 3
    code_availability: int = 0
    reproducibility_value: int = 3
    topic_relevance: int = 3
    method_type: str = "unknown"
    limitations: list[str] = field(default_factory=list)
    blocking_questions: list[str] = field(default_factory=list)
    risk_penalty: float = 1.0
    audit_conclusion: str = "needs_review"
    status: str = "audited"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PaperPriorityScore:
    paper_id: str
    title: str
    method_type: str
    priority: float
    topic_relevance: int
    reproducibility_value: int
    code_availability: int
    evidence_quality: int
    method_diversity_bonus: float
    risk_penalty: float
    selected: bool = False
    reason: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ObsidianNotePlan:
    note_id: str
    path: str
    title: str
    frontmatter: dict[str, str] = field(default_factory=dict)
    wikilinks: list[str] = field(default_factory=list)
    sections: list[str] = field(default_factory=list)
    status: str = "draft"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ExperimentTask:
    experiment_id: str
    paper_id: str
    title: str
    repo_url: str
    proposed_command: str
    expected_output: str
    selection_reason: str
    status: str = "planned"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class EnvironmentSnapshot:
    platform: str
    python: str
    cwd: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class CommandSpec:
    argv: list[str] = field(default_factory=list)
    shell: bool = False
    timeout_seconds: int = 0
    working_dir: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ExperimentReview:
    result: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ExperimentLog:
    run_id: str
    experiment_id: str
    paper_id: str
    repo_url: str
    mode: str
    environment: EnvironmentSnapshot
    command: CommandSpec
    status: str = "planned"
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    exit_code: int | None = None
    stdout_summary: str = ""
    stderr_summary: str = ""
    failure_type: str = ""
    review: ExperimentReview = field(default_factory=lambda: ExperimentReview(result="planned_only"))

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RunRecord:
    run_id: str
    experiment_id: str
    paper_id: str
    command: str
    status: str
    stdout_summary: str = ""
    stderr_summary: str = ""
    failure_type: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ReviewRecord:
    review_id: str
    citation_check: str
    metric_check: str
    boundary_check: str
    unresolved_questions: list[str] = field(default_factory=list)
    status: str = "draft"

    def to_dict(self) -> dict:
        return asdict(self)
