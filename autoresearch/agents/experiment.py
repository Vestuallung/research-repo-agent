from __future__ import annotations

import os
import platform
import sys

from autoresearch.schemas import (
    CommandSpec,
    EnvironmentSnapshot,
    ExperimentLog,
    ExperimentReview,
    ExperimentTask,
    PaperCandidate,
    PaperPriorityScore,
)


def make_experiment_task(score: PaperPriorityScore, candidate: PaperCandidate) -> ExperimentTask:
    return ExperimentTask(
        experiment_id=f"{candidate.paper_id}-smoke",
        paper_id=candidate.paper_id,
        title=candidate.title,
        repo_url=candidate.code_url,
        proposed_command="inspect repository README, dependency files, and documented demo command",
        expected_output="minimal install or help/demo command can be identified",
        selection_reason=score.reason,
    )


def record_planned_smoke(task: ExperimentTask) -> ExperimentLog:
    return ExperimentLog(
        run_id=f"{task.experiment_id}-planned",
        experiment_id=task.experiment_id,
        paper_id=task.paper_id,
        repo_url=task.repo_url,
        mode="planned",
        environment=EnvironmentSnapshot(
            platform=platform.system().lower(),
            python=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            cwd=os.getcwd(),
        ),
        command=CommandSpec(
            argv=["inspect", "repository", "metadata"],
            shell=False,
            timeout_seconds=0,
            working_dir="",
        ),
        status="planned",
        stdout_summary="Smoke test selected after paper audit. Execution is not run automatically in v0.",
        failure_type="not_run",
        review=ExperimentReview(
            result="planned_only",
            notes=[task.selection_reason, "external repository commands are not executed by default"],
        ),
    )
