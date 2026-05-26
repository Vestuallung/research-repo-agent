from __future__ import annotations

from pathlib import Path

from autoresearch.io import write_text
from autoresearch.schemas import ExperimentLog, ExperimentTask, PaperAudit, PaperCandidate, ResearchBrief, ReviewRecord


def write_vault(
    root: Path,
    brief: ResearchBrief | None,
    candidates: list[PaperCandidate],
    audits: list[PaperAudit],
    experiments: list[ExperimentTask],
    runs: list[ExperimentLog],
    review: ReviewRecord | None = None,
) -> None:
    vault = root / "vault"
    title = brief.topic if brief else "Research Topic"
    write_text(vault / "总索引.md", _index(title, candidates, experiments))
    write_text(vault / "主题地图.md", _topic_map(title, candidates, audits))
    write_text(vault / "调研方向.md", _brief_note(brief))
    write_text(vault / "论文总表.md", _paper_table(candidates, audits))
    write_text(vault / "gaps.md", _gaps(audits))
    for candidate in candidates:
        audit = next((a for a in audits if a.paper_id == candidate.paper_id), None)
        write_text(vault / "papers" / f"{candidate.paper_id}.md", _paper_note(candidate, audit))
    for audit in audits:
        write_text(vault / "reviews" / f"{audit.paper_id}-review.md", _audit_note(audit))
    for task in experiments:
        write_text(vault / "experiments" / f"{task.experiment_id}.md", _experiment_note(task))
    for run in runs:
        write_text(vault / "logs" / f"{run.run_id}.md", _run_note(run))
    if review:
        write_text(vault / "reviews" / "framework-review.md", _framework_review(review))


def _index(title: str, candidates: list[PaperCandidate], experiments: list[ExperimentTask]) -> str:
    return "\n".join(
        [
            f"# {title}",
            "",
            "- [[调研方向]]",
            "- [[主题地图]]",
            "- [[论文总表]]",
            "- [[gaps]]",
            "",
            f"- Papers: {len(candidates)}",
            f"- Smoke experiments: {len(experiments)}",
        ]
    )


def _topic_map(title: str, candidates: list[PaperCandidate], audits: list[PaperAudit]) -> str:
    lines = [f"# 主题地图: {title}", ""]
    methods = sorted({c.method_type for c in candidates})
    for method in methods:
        lines.extend([f"## {method}", ""])
        for c in candidates:
            if c.method_type == method:
                lines.append(f"- [[{c.paper_id}]]")
        lines.append("")
    if audits:
        lines.extend(["## 审查状态", ""])
        for a in audits:
            lines.append(f"- [[{a.paper_id}-review]]: {a.audit_conclusion}")
    return "\n".join(lines)


def _brief_note(brief: ResearchBrief | None) -> str:
    if not brief:
        return "# 调研方向\n\nNo brief found."
    lines = [
        "# 调研方向",
        "",
        f"- topic: {brief.topic}",
        f"- goal: {brief.goal}",
        f"- status: {brief.status}",
        "",
        "## Questions",
        "",
    ]
    lines.extend(f"- {q}" for q in brief.questions)
    return "\n".join(lines)


def _paper_table(candidates: list[PaperCandidate], audits: list[PaperAudit]) -> str:
    audit_map = {a.paper_id: a for a in audits}
    lines = ["# 论文总表", "", "| Paper | Method | Relevance | Audit | Code |", "|---|---|---:|---|---|"]
    for c in candidates:
        audit = audit_map.get(c.paper_id)
        audit_status = audit.audit_conclusion if audit else "not_audited"
        code = "yes" if c.code_url else "no"
        lines.append(f"| [[{c.paper_id}]] | {c.method_type} | {c.relevance} | {audit_status} | {code} |")
    return "\n".join(lines)


def _gaps(audits: list[PaperAudit]) -> str:
    lines = ["# gaps", ""]
    for audit in audits:
        for item in audit.blocking_questions:
            lines.append(f"- {audit.paper_id}: {item}")
    return "\n".join(lines)


def _paper_note(candidate: PaperCandidate, audit: PaperAudit | None) -> str:
    lines = [
        "---",
        "type: paper",
        f"paper_id: {candidate.paper_id}",
        "status: draft",
        "---",
        "",
        f"# {candidate.title}",
        "",
        "## Metadata",
        "",
        f"- url: {candidate.url}",
        f"- code: {candidate.code_url or 'none'}",
        f"- method_type: {candidate.method_type}",
        f"- relevance: {candidate.relevance}",
        "",
        "## Main Claims",
        "",
    ]
    if audit:
        lines.extend(f"- {claim}" for claim in audit.main_claims)
        lines.extend(["", "## Smoke Test Priority", "", f"- audit_conclusion: {audit.audit_conclusion}"])
    else:
        lines.append("- not audited")
    lines.extend(["", "## Related Notes", "", "- [[论文总表]]"])
    return "\n".join(lines)


def _audit_note(audit: PaperAudit) -> str:
    lines = [
        "---",
        "type: paper_review",
        f"paper_id: {audit.paper_id}",
        "status: draft",
        "---",
        "",
        f"# Review: {audit.title}",
        "",
        f"- evidence_quality: {audit.evidence_quality}",
        f"- code_availability: {audit.code_availability}",
        f"- reproducibility_value: {audit.reproducibility_value}",
        f"- risk_penalty: {audit.risk_penalty}",
        f"- conclusion: {audit.audit_conclusion}",
        "",
        "## Blocking Questions",
        "",
    ]
    lines.extend(f"- {q}" for q in audit.blocking_questions)
    return "\n".join(lines)


def _experiment_note(task: ExperimentTask) -> str:
    return "\n".join(
        [
            "---",
            "type: smoke_test",
            f"paper_id: {task.paper_id}",
            f"experiment_id: {task.experiment_id}",
            f"status: {task.status}",
            "---",
            "",
            f"# Smoke Test: {task.title}",
            "",
            f"- repository: {task.repo_url}",
            f"- proposed_command: {task.proposed_command}",
            f"- expected_output: {task.expected_output}",
            f"- selection_reason: {task.selection_reason}",
        ]
    )


def _run_note(run: ExperimentLog) -> str:
    return "\n".join(
        [
            f"# Run: {run.run_id}",
            "",
            f"- experiment_id: {run.experiment_id}",
            f"- paper_id: {run.paper_id}",
            f"- repo_url: {run.repo_url}",
            f"- mode: {run.mode}",
            f"- command: {' '.join(run.command.argv)}",
            f"- status: {run.status}",
            f"- failure_type: {run.failure_type}",
            f"- review_result: {run.review.result}",
            f"- platform: {run.environment.platform}",
            f"- python: {run.environment.python}",
            f"- cwd: {run.environment.cwd}",
            "",
            "## stdout",
            "",
            run.stdout_summary,
            "",
            "## Review Notes",
            "",
            *[f"- {note}" for note in run.review.notes],
        ]
    )


def _framework_review(review: ReviewRecord) -> str:
    lines = [
        "# Framework Review",
        "",
        f"- citation_check: {review.citation_check}",
        f"- metric_check: {review.metric_check}",
        f"- boundary_check: {review.boundary_check}",
        f"- status: {review.status}",
        "",
        "## Unresolved Questions",
        "",
    ]
    lines.extend(f"- {q}" for q in review.unresolved_questions)
    return "\n".join(lines)
