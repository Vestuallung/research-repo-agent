# Research Repro Agent

Research Repro Agent is a reusable workflow template for turning paper reading into a reviewable research process. It combines three things that usually get mixed together too early: a paper library, a small runnable experiment, and an Agent-assisted writing and review loop.

The goal is practical: a classmate should be able to clone the repository, run the demo, inspect the generated report, and then reuse the same workflow for a different research topic.

## What This Gives You

- A minimal CLI that reads a structured paper evaluation and scans a local repository.
- A demo report showing paper signals, repository signals, reproduction risks, and next actions.
- A reusable workflow for literature review, experiment notes, Agent drafting, and human recheck.
- Templates for a project outline and an Agent write-review protocol.

## Four-Step Start

1. Install dependencies.

   `python -m pip install -r requirements.txt`

2. Run the demo.

   `bash scripts/run_demo.sh`

3. Read the generated report.

   `examples/demo_reproduce_report.md`

4. Reuse the workflow for your own project.

   Start from `docs/reusable_research_workflow.md`, then write your outline with `docs/project_outline_template.md`, and use `docs/agent_write_review_protocol.md` whenever an Agent writes or revises notes.

## Manual CLI Usage

The demo script is only a wrapper around this command:

`PYTHONPATH=src python -m research_repro_agent.cli --paper-eval examples/hneurons_evaluation.json --repo . --out examples/demo_reproduce_report.md`

Expected terminal result:

`status       : completed`

## How To Reuse This For Another Research Topic

Use the repository as a scaffold rather than a finished paper. Replace the sample evaluation JSON with your own structured paper evaluation, point `--repo` to the codebase you want to inspect, and keep every Agent-generated conclusion in draft status until it has been checked against sources and experiment outputs.

Recommended project rhythm:

- Collect papers into a small, structured library.
- Write one paper card per paper.
- Group cards into a topic map and a first outline.
- Run the CLI or an equivalent experiment script to produce an auditable report.
- Let an Agent draft summaries and comparisons from existing notes.
- Recheck citations, metrics, and conclusion boundaries before writing the final version.

## Repository Layout

- `src/research_repro_agent`: minimal CLI and Agent pipeline.
- `examples`: sample paper evaluation and generated demo report.
- `scripts/run_demo.sh`: one-command local demo.
- `docs/reusable_research_workflow.md`: reusable research workflow.
- `docs/agent_write_review_protocol.md`: Agent drafting and human recheck rules.
- `docs/project_outline_template.md`: project outline template.

## Current Status

This is a small workflow template, not a full automation platform. The included sample demonstrates the structure: Paper Agent extracts claims and risks, Repo Agent scans files, Planner Agent creates a reproduction checklist, and Reporter writes a markdown report.
