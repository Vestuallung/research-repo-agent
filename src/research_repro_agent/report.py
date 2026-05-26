from __future__ import annotations

from .models import PaperSignal, RepoSignal, ReproPlan
from .paper_agent import summarize_claims


def render_markdown(paper: PaperSignal, repo: RepoSignal, plan: ReproPlan) -> str:
    lines: list[str] = []
    lines.append(f"# Reproduction Agent Report: {paper.title}")
    lines.append("")
    lines.append("## Agent Flow")
    lines.append("")
    lines.append("Paper Agent extracted claims, support levels, weaknesses, and red flags.")
    lines.append("Repo Agent scanned local files to locate entrypoints, configs, tests, and dependency manifests.")
    lines.append("Planner Agent converted both signals into a minimal reproduction checklist.")
    lines.append("")
    lines.append("## Paper Signals")
    lines.append("")
    lines.append(f"- Primary type: `{paper.primary_type}`")
    lines.append(f"- Tags: `{', '.join(paper.tags) or 'none'}`")
    lines.append(f"- Final score: `{paper.scores.get('overall_score_final', 'unknown')}`")
    lines.append(f"- Risk level: `{plan.risk_level}`")
    lines.append("")
    lines.append("## Claims")
    lines.append("")
    for row in summarize_claims(paper):
        lines.append(f"- {row}")
    lines.append("")
    lines.append("## Repository Signals")
    lines.append("")
    lines.append(f"- Root: `{repo.root}`")
    lines.append(f"- Files scanned: `{len(repo.files)}`")
    lines.append(f"- Entrypoints: `{', '.join(repo.likely_entrypoints) or 'none'}`")
    lines.append(f"- Dependencies: `{', '.join(repo.dependency_files) or 'none'}`")
    lines.append(f"- Configs: `{', '.join(repo.config_files[:8]) or 'none'}`")
    lines.append(f"- Tests: `{', '.join(repo.test_files[:8]) or 'none'}`")
    lines.append("")
    lines.append("## Setup Steps")
    lines.append("")
    for item in plan.setup_steps:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Smoke Tests")
    lines.append("")
    for item in plan.smoke_tests:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Reproduction Tasks")
    lines.append("")
    for item in plan.reproduction_tasks:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Agent Notes")
    lines.append("")
    for item in plan.agent_notes:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Blocking Questions")
    lines.append("")
    for item in paper.blocking_questions[:5]:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)
