from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PaperSignal:
    title: str
    primary_type: str
    tags: list[str]
    claims: list[dict]
    scores: dict
    flags: dict
    weaknesses: list[str]
    blocking_questions: list[str]


@dataclass
class RepoSignal:
    root: str
    files: list[str]
    likely_entrypoints: list[str] = field(default_factory=list)
    config_files: list[str] = field(default_factory=list)
    dependency_files: list[str] = field(default_factory=list)
    data_files: list[str] = field(default_factory=list)
    test_files: list[str] = field(default_factory=list)


@dataclass
class ReproPlan:
    objective: str
    risk_level: str
    setup_steps: list[str]
    smoke_tests: list[str]
    reproduction_tasks: list[str]
    agent_notes: list[str]
