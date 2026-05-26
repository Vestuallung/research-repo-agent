from __future__ import annotations

import argparse
import sys

from autoresearch.orchestrator import ResearchWorkspace


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="research-repo")
    parser.add_argument("--root", default=".", help="Workspace root. Defaults to current directory.")
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser("init")
    p.add_argument("--topic", required=True)
    p.add_argument("--goal", default="")
    p.add_argument("--keywords", default="")
    p.add_argument("--exclude", action="append", default=[])
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("plan")
    p.set_defaults(func=cmd_plan)

    p = sub.add_parser("add-paper")
    p.add_argument("--title", required=True)
    p.add_argument("--url", required=True)
    p.add_argument("--paper-id", default="")
    p.add_argument("--authors", default="")
    p.add_argument("--year", default="")
    p.add_argument("--source", default="")
    p.add_argument("--code-url", default="")
    p.add_argument("--method-type", default="unknown")
    p.add_argument("--relevance", type=int, default=3)
    p.add_argument("--tags", default="")
    p.add_argument("--screening-reason", default="")
    p.set_defaults(func=cmd_add_paper)

    p = sub.add_parser("audit-paper")
    p.add_argument("--paper-id", required=True)
    p.set_defaults(func=cmd_audit_paper)

    p = sub.add_parser("rank-papers")
    p.set_defaults(func=cmd_rank_papers)

    p = sub.add_parser("select-experiments")
    p.add_argument("--top-k", type=int, default=3)
    p.set_defaults(func=cmd_select_experiments)

    p = sub.add_parser("run-smoke")
    p.add_argument("--selected", action="store_true")
    p.set_defaults(func=cmd_run_smoke)

    p = sub.add_parser("write-vault")
    p.set_defaults(func=cmd_write_vault)

    p = sub.add_parser("review")
    p.set_defaults(func=cmd_review)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


def workspace(args) -> ResearchWorkspace:
    return ResearchWorkspace(args.root)


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def cmd_init(args) -> int:
    brief = workspace(args).init(
        args.topic,
        goal=args.goal,
        keywords=split_csv(args.keywords),
        exclusions=args.exclude,
    )
    print(f"initialized research workspace: {brief.topic}")
    print("wrote artifacts/briefs/current.json")
    return 0


def cmd_plan(args) -> int:
    workspace(args).plan()
    print("wrote artifacts/briefs/plan.md")
    return 0


def cmd_add_paper(args) -> int:
    candidate = workspace(args).add_paper(
        title=args.title,
        url=args.url,
        paper_id=args.paper_id,
        authors=split_csv(args.authors),
        year=args.year,
        source=args.source,
        code_url=args.code_url,
        method_type=args.method_type,
        relevance=args.relevance,
        tags=split_csv(args.tags),
        screening_reason=args.screening_reason,
    )
    print(f"registered paper: {candidate.paper_id}")
    return 0


def cmd_audit_paper(args) -> int:
    audit = workspace(args).audit_paper(args.paper_id)
    print(f"audited paper: {audit.paper_id}")
    print(f"conclusion: {audit.audit_conclusion}")
    return 0


def cmd_rank_papers(args) -> int:
    scores = workspace(args).rank_papers()
    print(f"ranked {len(scores)} audited papers")
    for score in scores[:5]:
        print(f"{score.paper_id}: priority={score.priority} reason={score.reason}")
    return 0


def cmd_select_experiments(args) -> int:
    tasks = workspace(args).select_experiments(top_k=args.top_k)
    print(f"selected {len(tasks)} smoke-test tasks")
    print("wrote artifacts/rankings/selected_experiments.json")
    return 0


def cmd_run_smoke(args) -> int:
    runs = workspace(args).run_smoke(selected_only=args.selected)
    print(f"recorded {len(runs)} planned smoke-test runs")
    return 0


def cmd_write_vault(args) -> int:
    workspace(args).write_vault()
    print("wrote Obsidian vault")
    return 0


def cmd_review(args) -> int:
    review = workspace(args).review()
    print(f"wrote review: {review.review_id}")
    print(f"status: {review.status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
