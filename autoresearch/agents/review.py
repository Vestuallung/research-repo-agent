from __future__ import annotations

from autoresearch.schemas import ExperimentLog, PaperAudit, ReviewRecord


def review_artifacts(audits: list[PaperAudit], runs: list[ExperimentLog]) -> ReviewRecord:
    unresolved: list[str] = []
    for audit in audits:
        unresolved.extend(f"{audit.paper_id}: {q}" for q in audit.blocking_questions[:2])
    citation_check = "paper audits exist" if audits else "no paper audits found"
    metric_check = "run records exist" if runs else "no run records found"
    boundary_check = "draft conclusions must remain bounded by audits and run records"
    return ReviewRecord(
        review_id="framework-review",
        citation_check=citation_check,
        metric_check=metric_check,
        boundary_check=boundary_check,
        unresolved_questions=unresolved[:12],
        status="needs_review" if unresolved else "checked",
    )
