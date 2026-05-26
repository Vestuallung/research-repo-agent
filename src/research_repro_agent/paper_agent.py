from __future__ import annotations

import json
from pathlib import Path

from .models import PaperSignal


def load_paper_signal(path: str | Path) -> PaperSignal:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    metadata = data.get("metadata", {})
    paper_type = data.get("paper_type", {})
    return PaperSignal(
        title=metadata.get("title", "Unknown paper"),
        primary_type=paper_type.get("primary_type", "unknown"),
        tags=paper_type.get("secondary_tags", []),
        claims=data.get("claim_table", []),
        scores=data.get("derived_scores", {}),
        flags=data.get("flags", {}),
        weaknesses=data.get("top_weaknesses", []),
        blocking_questions=data.get("blocking_questions", []),
    )


def summarize_claims(signal: PaperSignal) -> list[str]:
    rows: list[str] = []
    for claim in signal.claims:
        cid = claim.get("claim_id", "C?")
        text = claim.get("claim_text", "")
        support = claim.get("support_score", "?")
        rows.append(f"{cid}: support={support}/2; {text}")
    return rows
