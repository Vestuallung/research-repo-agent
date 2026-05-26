from __future__ import annotations

from .models import PaperSignal, RepoSignal, ReproPlan


def build_plan(paper: PaperSignal, repo: RepoSignal) -> ReproPlan:
    risk_level = "medium"
    if paper.flags.get("internal_contradiction_major") or paper.flags.get("main_claim_unsupported"):
        risk_level = "high"
    elif paper.scores.get("overall_score_final", 0) >= 70:
        risk_level = "low"

    setup_steps = []
    if repo.dependency_files:
        setup_steps.append(f"Install dependencies from {', '.join(repo.dependency_files[:3])}.")
    else:
        setup_steps.append("No dependency manifest found; inspect README or source imports manually.")

    if repo.config_files:
        setup_steps.append(f"Inspect config files: {', '.join(repo.config_files[:5])}.")

    smoke_tests = []
    if repo.test_files:
        smoke_tests.append("Run available tests before reproducing paper-level results.")
    if repo.likely_entrypoints:
        smoke_tests.append(f"Try a minimal dry run through {repo.likely_entrypoints[0]}.")
    else:
        smoke_tests.append("Locate the training or evaluation entrypoint before running experiments.")

    reproduction_tasks = [
        "Map each primary claim to the exact script, dataset, and metric needed for verification.",
        "Reproduce one table or figure before attempting full-scale experiments.",
        "Record missing seeds, run counts, compute setup, and judge prompts as blocking gaps.",
    ]

    agent_notes = [
        f"Paper type: {paper.primary_type}; tags: {', '.join(paper.tags) or 'none'}.",
        f"Detected {len(repo.files)} repository files, {len(repo.likely_entrypoints)} candidate entrypoints.",
    ]
    for weakness in paper.weaknesses[:3]:
        agent_notes.append(f"Risk from paper evaluation: {weakness}")

    return ReproPlan(
        objective=f"Prepare a minimal reproduction plan for: {paper.title}",
        risk_level=risk_level,
        setup_steps=setup_steps,
        smoke_tests=smoke_tests,
        reproduction_tasks=reproduction_tasks,
        agent_notes=agent_notes,
    )
