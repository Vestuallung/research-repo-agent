from __future__ import annotations

from pathlib import Path

from autoresearch.agents.audit import audit_candidate
from autoresearch.agents.direction import make_brief
from autoresearch.agents.experiment import make_experiment_task, record_planned_smoke
from autoresearch.agents.literature import make_candidate
from autoresearch.agents.obsidian import write_vault
from autoresearch.agents.ranking import rank_audits, select_for_smoke
from autoresearch.agents.review import review_artifacts
from autoresearch.io import ensure_workspace, iter_json_files, read_artifact, read_json, write_artifact, write_json, write_text
from autoresearch.schemas import (
    CommandSpec,
    EnvironmentSnapshot,
    ExperimentLog,
    ExperimentReview,
    ExperimentTask,
    PaperAudit,
    PaperCandidate,
    PaperPriorityScore,
    ResearchBrief,
    ReviewRecord,
)


class ResearchWorkspace:
    def __init__(self, root: Path | str = ".") -> None:
        self.root = Path(root)

    def init(self, topic: str, goal: str = "", keywords: list[str] | None = None, exclusions: list[str] | None = None) -> ResearchBrief:
        ensure_workspace(self.root)
        brief = make_brief(topic, goal=goal, keywords=keywords, exclusions=exclusions)
        write_artifact(
            self.root / "artifacts/briefs/current.json",
            artifact_type="research_brief",
            artifact_id="current",
            producer="DirectionAgent",
            status=brief.status,
            data=brief.to_dict(),
        )
        write_text(self.root / "vault/总索引.md", f"# {topic}\n\n- [[调研方向]]\n- [[论文总表]]")
        write_text(self.root / "vault/调研方向.md", f"# 调研方向\n\n{brief.goal}")
        write_text(self.root / "vault/论文总表.md", "# 论文总表\n")
        write_text(self.root / "vault/主题地图.md", "# 主题地图\n")
        return brief

    def plan(self) -> str:
        brief = self.load_brief()
        lines = [
            f"# Research Plan: {brief.topic}",
            "",
            f"- goal: {brief.goal}",
            f"- keywords: {', '.join(brief.keywords) or 'none'}",
            f"- exclusions: {', '.join(brief.exclusions) or 'none'}",
            "",
            "## Questions",
            "",
        ]
        lines.extend(f"- {q}" for q in brief.questions)
        lines.extend(["", "## Success Criteria", ""])
        lines.extend(f"- {item}" for item in brief.success_criteria)
        content = "\n".join(lines)
        write_text(self.root / "artifacts/briefs/plan.md", content)
        return content

    def add_paper(
        self,
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
        ensure_workspace(self.root)
        candidate = make_candidate(
            title=title,
            url=url,
            paper_id=paper_id,
            authors=authors,
            year=year,
            source=source,
            code_url=code_url,
            method_type=method_type,
            relevance=relevance,
            tags=tags,
            screening_reason=screening_reason,
        )
        write_artifact(
            self.root / "artifacts/papers" / f"{candidate.paper_id}.json",
            artifact_type="paper_candidate",
            artifact_id=candidate.paper_id,
            producer="LiteratureAgent",
            status=candidate.status,
            data=candidate.to_dict(),
        )
        return candidate

    def audit_paper(self, paper_id: str) -> PaperAudit:
        candidate = self.load_candidate(paper_id)
        audit = audit_candidate(candidate)
        write_artifact(
            self.root / "artifacts/audits" / f"{paper_id}.json",
            artifact_type="paper_audit",
            artifact_id=paper_id,
            producer="PaperAuditAgent",
            status=audit.status,
            data=audit.to_dict(),
        )
        return audit

    def rank_papers(self) -> list[PaperPriorityScore]:
        audits = self.load_audits()
        scores = rank_audits(audits)
        write_artifact(
            self.root / "artifacts/rankings/paper_priority.json",
            artifact_type="paper_priority_list",
            artifact_id="paper-priority",
            producer="ExperimentAgent",
            status="draft",
            data={"scores": [s.to_dict() for s in scores]},
        )
        return scores

    def select_experiments(self, top_k: int = 3) -> list[ExperimentTask]:
        scores = self.load_scores()
        if not scores:
            scores = self.rank_papers()
        selected_scores = select_for_smoke(scores, top_k=top_k)
        candidates = {c.paper_id: c for c in self.load_candidates()}
        tasks: list[ExperimentTask] = []
        for score in selected_scores:
            candidate = candidates.get(score.paper_id)
            if not candidate:
                continue
            task = make_experiment_task(score, candidate)
            tasks.append(task)
            write_artifact(
                self.root / "artifacts/experiments" / f"{task.experiment_id}.json",
                artifact_type="experiment_task",
                artifact_id=task.experiment_id,
                producer="ExperimentAgent",
                status=task.status,
                data=task.to_dict(),
            )
        write_artifact(
            self.root / "artifacts/rankings/selected_experiments.json",
            artifact_type="selected_experiments",
            artifact_id="selected-experiments",
            producer="ExperimentAgent",
            status="selected" if tasks else "blocked",
            data={
                "scores": [s.to_dict() for s in scores],
                "selected_experiment_ids": [task.experiment_id for task in tasks],
            },
        )
        return tasks

    def run_smoke(self, selected_only: bool = True) -> list[ExperimentLog]:
        tasks = self.load_experiments()
        runs: list[ExperimentLog] = []
        for task in tasks:
            run = record_planned_smoke(task)
            runs.append(run)
            write_artifact(
                self.root / "artifacts/experiments" / f"{run.run_id}.json",
                artifact_type="experiment_log",
                artifact_id=run.run_id,
                producer="ExperimentAgent",
                status=run.status,
                data=run.to_dict(),
            )
        return runs

    def write_vault(self) -> None:
        brief = self.safe_load_brief()
        review = self.safe_load_review()
        write_vault(
            self.root,
            brief,
            self.load_candidates(),
            self.load_audits(),
            self.load_experiments(),
            self.load_runs(),
            review,
        )

    def review(self) -> ReviewRecord:
        review = review_artifacts(self.load_audits(), self.load_runs())
        write_artifact(
            self.root / "artifacts/reviews/review.json",
            artifact_type="review_record",
            artifact_id=review.review_id,
            producer="ReviewAgent",
            status=review.status,
            data=review.to_dict(),
        )
        return review

    def load_brief(self) -> ResearchBrief:
        data = read_artifact(self.root / "artifacts/briefs/current.json")
        return ResearchBrief(**data)

    def safe_load_brief(self) -> ResearchBrief | None:
        path = self.root / "artifacts/briefs/current.json"
        if not path.exists():
            return None
        return ResearchBrief(**read_artifact(path))

    def load_candidate(self, paper_id: str) -> PaperCandidate:
        return PaperCandidate(**read_artifact(self.root / "artifacts/papers" / f"{paper_id}.json"))

    def load_candidates(self) -> list[PaperCandidate]:
        return [PaperCandidate(**read_artifact(path)) for path in iter_json_files(self.root / "artifacts/papers")]

    def load_audits(self) -> list[PaperAudit]:
        return [PaperAudit(**read_artifact(path)) for path in iter_json_files(self.root / "artifacts/audits")]

    def load_scores(self) -> list[PaperPriorityScore]:
        path = self.root / "artifacts/rankings/paper_priority.json"
        if not path.exists():
            return []
        data = read_artifact(path)
        rows = data.get("scores", data) if isinstance(data, dict) else data
        for row in rows:
            row.setdefault("method_type", "unknown")
        return [PaperPriorityScore(**row) for row in rows]

    def load_experiments(self) -> list[ExperimentTask]:
        tasks: list[ExperimentTask] = []
        for path in iter_json_files(self.root / "artifacts/experiments"):
            data = read_artifact(path)
            if "experiment_id" in data and "repo_url" in data and "proposed_command" in data:
                tasks.append(ExperimentTask(**data))
        return tasks

    def load_runs(self) -> list[ExperimentLog]:
        runs: list[ExperimentLog] = []
        for path in iter_json_files(self.root / "artifacts/experiments"):
            data = read_artifact(path)
            if "run_id" in data:
                runs.append(_experiment_log_from_data(data))
        return runs

    def safe_load_review(self) -> ReviewRecord | None:
        path = self.root / "artifacts/reviews/review.json"
        if not path.exists():
            return None
        return ReviewRecord(**read_artifact(path))


def _experiment_log_from_data(data: dict) -> ExperimentLog:
    env = data.get("environment") or {"platform": "unknown", "python": "unknown", "cwd": ""}
    command = data.get("command") or {"argv": [str(data.get("command", ""))], "shell": False, "timeout_seconds": 0, "working_dir": ""}
    if isinstance(command, str):
        command = {"argv": [command], "shell": False, "timeout_seconds": 0, "working_dir": ""}
    review = data.get("review") or {"result": "legacy", "notes": []}
    data = dict(data)
    data.setdefault("repo_url", "")
    data.setdefault("mode", "planned")
    data.setdefault("status", "planned")
    data["environment"] = EnvironmentSnapshot(**env)
    data["command"] = CommandSpec(**command)
    data["review"] = ExperimentReview(**review)
    return ExperimentLog(**data)
