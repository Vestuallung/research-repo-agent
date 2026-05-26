# Experiment Log Specification

Smoke tests are recorded as normalized experiment logs. In v0, `run-smoke` creates planned logs by default and does not execute external repositories.

## Purpose

The experiment log is the audit trail for research execution. It records why a paper was selected, what would be run, what environment was observed, and why a result is missing or blocked.

## Artifact Type

Use `experiment_log`.

Example:

```json
{
  "schema_version": "autoresearch.v0",
  "artifact_type": "experiment_log",
  "artifact_id": "sinktrack-smoke-planned",
  "producer": "ExperimentAgent",
  "status": "planned",
  "data": {
    "run_id": "sinktrack-smoke-planned",
    "experiment_id": "sinktrack-smoke",
    "paper_id": "sinktrack",
    "repo_url": "https://github.com/example/sinktrack",
    "mode": "planned",
    "environment": {
      "platform": "darwin",
      "python": "3.13",
      "cwd": "."
    },
    "command": {
      "argv": ["inspect", "repository", "metadata"],
      "shell": false,
      "timeout_seconds": 0,
      "working_dir": ""
    },
    "inputs": [],
    "outputs": [],
    "artifacts": [],
    "exit_code": null,
    "status": "planned",
    "stdout_summary": "",
    "stderr_summary": "",
    "failure_type": "not_run",
    "review": {
      "result": "planned_only",
      "notes": ["selected after audit ranking"]
    }
  }
}
```

## Modes

- `planned`: selected after audit ranking, not executed.
- `executed`: command was actually run.
- `imported`: result was imported from an external log.

## Failure Types

- `not_run`
- `missing_repo`
- `missing_dependency_manifest`
- `missing_entrypoint`
- `install_failed`
- `command_failed`
- `timeout`
- `data_missing`
- `environment_incompatible`
- `unsafe_command`
- `unknown`

## Execution Policy

The default `run-smoke` behavior is planned-only. Future execution support must use a separate explicit flag or command and must record:

- command argv;
- timeout;
- working directory;
- exit code;
- stdout and stderr summaries;
- generated artifacts;
- failure type.

No heavy training or long benchmark run should be treated as a smoke test.
