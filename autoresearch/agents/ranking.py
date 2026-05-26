from __future__ import annotations

from collections import Counter

from autoresearch.schemas import PaperAudit, PaperPriorityScore


def rank_audits(audits: list[PaperAudit]) -> list[PaperPriorityScore]:
    method_counts = Counter(a.method_type for a in audits)
    scores: list[PaperPriorityScore] = []
    for audit in audits:
        diversity_bonus = 1.0 if method_counts[audit.method_type] == 1 else 0.5
        priority = (
            0.30 * audit.topic_relevance
            + 0.25 * audit.reproducibility_value
            + 0.20 * audit.code_availability
            + 0.15 * audit.evidence_quality
            + 0.10 * diversity_bonus
            - audit.risk_penalty
        )
        reason = "eligible for smoke test" if audit.code_availability > 0 and priority > 1.5 else "skipped by default"
        scores.append(
            PaperPriorityScore(
                paper_id=audit.paper_id,
                title=audit.title,
                method_type=audit.method_type,
                priority=round(priority, 3),
                topic_relevance=audit.topic_relevance,
                reproducibility_value=audit.reproducibility_value,
                code_availability=audit.code_availability,
                evidence_quality=audit.evidence_quality,
                method_diversity_bonus=diversity_bonus,
                risk_penalty=audit.risk_penalty,
                reason=reason,
            )
        )
    return sorted(scores, key=lambda row: row.priority, reverse=True)


def select_for_smoke(scores: list[PaperPriorityScore], top_k: int = 3) -> list[PaperPriorityScore]:
    selected: list[PaperPriorityScore] = []
    seen_methods: set[str] = set()
    eligible = [score for score in scores if score.code_availability > 0 and score.priority > 1.5]

    for score in scores:
        score.selected = False
        if score not in eligible:
            score.reason = "not selected: missing code or low priority"

    for score in eligible:
        if len(selected) >= top_k:
            break
        if score.method_type in seen_methods:
            continue
        score.selected = True
        score.reason = "selected after audit ranking with method diversity"
        selected.append(score)
        seen_methods.add(score.method_type)

    for score in eligible:
        if len(selected) >= top_k:
            break
        if score.selected:
            continue
        score.selected = True
        score.reason = "selected after audit ranking"
        selected.append(score)

    for score in eligible:
        if not score.selected:
            score.reason = "not selected: top-k limit"
    return selected
