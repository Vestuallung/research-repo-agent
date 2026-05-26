# Research Repro Agent

Research Repro Agent is a lightweight multi-agent prototype for AI paper evaluation and experiment reproduction planning. It turns a structured paper review into a concrete checklist for understanding a research codebase, deciding what to run first, and identifying which missing details block a trustworthy reproduction.

This repository is intentionally small: it is built as a demonstrable MVP for token-plan review, coursework research, and paper-reading workflows. The current version runs locally with only the Python standard library.

## Problem

Reproducing an AI paper is rarely just running one command. Important details are scattered across the paper, appendix, README, config files, training scripts, evaluation scripts, issue threads, and terminal logs. A reader has to answer several questions before spending real compute:

- What are the paper's primary claims?
- Which claims are directly supported by evidence?
- Which scripts and configs correspond to those claims?
- Are there missing seeds, run counts, prompts, datasets, or compute details?
- What is the smallest smoke test before attempting full reproduction?

Research Repro Agent packages that workflow as an agent pipeline.

## Agent Architecture

Paper Agent extracts research-level signals from a standardized evaluation JSON:

- paper type and topic tags
- primary claims and support scores
- quality, interest, and overall scores
- red flags and blocking questions
- top weaknesses that affect reproducibility

Repo Agent scans a local research repository:

- dependency manifests such as `pyproject.toml`, `requirements.txt`, and `environment.yml`
- candidate entrypoints such as `cli.py`, `train.py`, `eval.py`, `main.py`, and scripts
- configuration files
- tests and example data

Planner Agent combines paper-level risk with code-level structure:

- assigns a reproduction risk level
- proposes setup steps
- suggests smoke tests
- turns weaknesses into concrete reproduction tasks

Reporter writes a markdown report that can be attached to a lab note, GitHub issue, course project, or research log.

## Quick Demo

From the repository root:

`PYTHONPATH=src python -m research_repro_agent.cli --paper-eval examples/hneurons_evaluation.json --repo . --out examples/demo_reproduce_report.md`

Expected output:

`Wrote examples/demo_reproduce_report.md`

The generated sample report is available at `examples/demo_reproduce_report.md`.

## Included Seed Material

This project reuses an earlier AI paper evaluation protocol as its first evaluation kernel:

- `examples/AI_Paper_Evaluation_Protocol.md`
- `examples/hneurons_evaluation.json`

The sample evaluation is used to demonstrate the agent flow. It is not presented as a full reproduction of the referenced paper.

## Current Capabilities

- Reads a standardized paper evaluation JSON.
- Extracts claims, support levels, scores, flags, weaknesses, and blocking questions.
- Scans repository structure without external dependencies.
- Detects likely entrypoints, dependencies, configs, tests, and example data.
- Generates a reproduction-oriented markdown report.

## Planned Extensions

- PDF and arXiv ingestion for long-context paper reading.
- LLM-assisted claim extraction from raw papers.
- Codebase-level semantic analysis for large research repositories.
- Terminal log diagnosis through a Debugger Agent.
- Patch or issue generation for missing dependencies, broken commands, and unclear configs.

## Why This Needs Token Budget

The useful version of this tool requires repeated long-context model calls over papers, code trees, configs, and terminal logs. A realistic workflow may include paper parsing, multi-agent planning, repository summarization, failure diagnosis, and report generation across several iterations. This makes it a practical token-consuming research assistant rather than a single-turn chatbot demo.

## Example Application Identity

I am a computer science undergraduate building an Agent-assisted workflow for AI paper evaluation and experiment reproduction. The goal is to help students and early-stage researchers connect paper claims, evidence quality, repository structure, and reproduction risk before spending time or compute on experiments.

## Repository Layout

- `src/research_repro_agent`: local agent pipeline implementation
- `examples`: protocol, sample evaluation, and generated demo report
- `docs/workflow.md`: workflow description
- `docs/xiaomi_token_plan_answer.md`: draft text for token-plan application

## Status

Prototype. The repository is suitable for demonstrating the workflow, attaching to an application form, and extending into a richer long-context Agent system.
