from __future__ import annotations

from autoresearch.schemas import ResearchBrief


def make_brief(topic: str, goal: str = "", keywords: list[str] | None = None, exclusions: list[str] | None = None) -> ResearchBrief:
    topic = topic.strip()
    inferred_keywords = keywords or [word for word in topic.replace("-", " ").split() if len(word) > 3]
    return ResearchBrief(
        topic=topic,
        goal=goal or f"Audit the research landscape around {topic}.",
        keywords=inferred_keywords[:8],
        exclusions=exclusions or [],
        questions=[
            f"What are the main research directions around {topic}?",
            "Which claims are supported by concrete evidence?",
            "Which papers provide runnable code or reproducible experiments?",
            "Which audited papers deserve smoke tests first?",
        ],
        success_criteria=[
            "A scoped research brief exists.",
            "Paper candidates are registered with metadata.",
            "Audits distinguish claims, evidence, risks, and code availability.",
            "Only audited high-priority papers are selected for smoke tests.",
            "The Obsidian vault can trace conclusions back to artifacts.",
        ],
    )
