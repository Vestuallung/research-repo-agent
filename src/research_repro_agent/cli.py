from __future__ import annotations

import argparse
from pathlib import Path

from .paper_agent import load_paper_signal
from .planner_agent import build_plan
from .repo_agent import scan_repo
from .report import render_markdown


def _clip(text: str, limit: int = 78) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def print_demo_summary(paper, repo, plan, out_path: str) -> None:
    print("Research Repro Agent")
    print("=" * 72)
    print("[1/4] Paper Agent")
    print(f"  title        : {_clip(paper.title)}")
    print(f"  type/tags    : {paper.primary_type} / {', '.join(paper.tags) or 'none'}")
    print(f"  claims       : {len(paper.claims)} extracted")
    print(f"  final score  : {paper.scores.get('overall_score_final', 'unknown')}")
    print("")
    print("[2/4] Repo Agent")
    print(f"  files        : {len(repo.files)} scanned")
    print(f"  entrypoints  : {', '.join(repo.likely_entrypoints[:3]) or 'none'}")
    print(f"  dependencies : {', '.join(repo.dependency_files[:3]) or 'none'}")
    print(f"  configs      : {', '.join(repo.config_files[:3]) or 'none'}")
    print("")
    print("[3/4] Planner Agent")
    print(f"  risk level   : {plan.risk_level}")
    for item in plan.smoke_tests[:2]:
        print(f"  smoke test   : {_clip(item)}")
    print("")
    print("[4/4] Reporter")
    print(f"  report       : {out_path}")
    print("  status       : completed")
    print("=" * 72)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a research reproduction agent report.")
    parser.add_argument("--paper-eval", required=True, help="Path to a standardized paper evaluation JSON.")
    parser.add_argument("--repo", required=True, help="Path to the repository to inspect.")
    parser.add_argument("--out", default="reproduce_report.md", help="Output markdown report path.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    paper = load_paper_signal(args.paper_eval)
    repo = scan_repo(args.repo)
    plan = build_plan(paper, repo)
    report = render_markdown(paper, repo, plan)
    Path(args.out).write_text(report, encoding="utf-8")
    print_demo_summary(paper, repo, plan, args.out)


if __name__ == "__main__":
    main()
