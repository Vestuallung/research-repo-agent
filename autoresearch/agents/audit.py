from __future__ import annotations

from autoresearch.schemas import PaperAudit, PaperCandidate


def audit_candidate(candidate: PaperCandidate) -> PaperAudit:
    code_availability = 5 if candidate.code_url else 0
    evidence_quality = 3
    reproducibility_value = 4 if candidate.code_url else 2
    risk_penalty = 0.5 if candidate.code_url else 2.0
    conclusion = "smoke_candidate" if candidate.code_url and candidate.relevance >= 3 else "needs_review"
    return PaperAudit(
        paper_id=candidate.paper_id,
        title=candidate.title,
        main_claims=[
            "Main claims require structured extraction from the paper text.",
            "Current audit is metadata-based and should be upgraded with full paper reading.",
        ],
        evidence_quality=evidence_quality,
        code_availability=code_availability,
        reproducibility_value=reproducibility_value,
        topic_relevance=candidate.relevance,
        method_type=candidate.method_type,
        limitations=[
            "Full-text paper audit has not been performed yet.",
            "Evidence quality is a placeholder until source-level review is available.",
        ],
        blocking_questions=[
            "Which claims are central to the paper?",
            "Which table, figure, proof, or benchmark supports each claim?",
            "Does the linked repository contain a documented minimal demo?",
        ],
        risk_penalty=risk_penalty,
        audit_conclusion=conclusion,
    )
