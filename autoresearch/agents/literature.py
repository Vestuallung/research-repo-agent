from __future__ import annotations

from autoresearch.io import slugify
from autoresearch.schemas import PaperCandidate


def make_candidate(
    *,
    title: str,
    url: str,
    paper_id: str = "",
    authors: list[str] | None = None,
    year: str = "",
    source: str = "",
    code_url: str = "",
    method_type: str = "unknown",
    relevance: int = 3,
    tags: list[str] | None = None,
    screening_reason: str = "",
) -> PaperCandidate:
    pid = paper_id or slugify(title or url)
    return PaperCandidate(
        paper_id=pid,
        title=title or pid,
        url=url,
        authors=authors or [],
        year=year,
        source=source,
        code_url=code_url,
        method_type=method_type,
        relevance=max(1, min(5, relevance)),
        tags=tags or [],
        screening_reason=screening_reason or "Registered for audit.",
    )
