from __future__ import annotations

import argparse
from pathlib import Path

from .paper_agent import load_paper_signal
from .planner_agent import build_plan
from .repo_agent import scan_repo
from .report import render_markdown


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
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
