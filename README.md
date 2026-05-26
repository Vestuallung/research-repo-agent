# Research Repro Agent

中文说明: [README.zh-CN.md](README.zh-CN.md)

Research Repro Agent is an AutoResearch-style framework for automated research auditing. It coordinates research direction planning, paper discovery, paper review, Obsidian vault generation, experiment candidate ranking, and smoke-test recording.

The project is moving away from a single paper-reproduction demo toward a staged research automation system. The current implementation is intentionally conservative: it writes structured artifacts, keeps Agent-produced content auditable, and only runs or proposes lightweight smoke tests after papers have passed an explicit audit stage.

## Concept

The framework is inspired by two ideas:

- Karpathy-style `autoresearch`: a human-authored `program.md` defines the research loop, fixed rules constrain what the agent may touch, and measurable outcomes decide whether progress is real.
- Multi-agent autonomous research pipelines such as AutoResearchClaw: research is iterative, failures become information, reports must be verifiable, and human review remains part of the loop.

This repository adapts those ideas to literature-driven research:

```text
topic
  -> direction planning
  -> paper candidate registration
  -> paper audit
  -> candidate ranking
  -> Obsidian vault generation
  -> selected smoke tests
  -> review records
```

## Agent Roles

- `MainAgent`: orchestrates stages and artifact locations.
- `DirectionAgent`: turns a topic into a research brief.
- `LiteratureAgent`: registers paper candidates and search metadata.
- `PaperAuditAgent`: reviews claims, evidence, code availability, and reproducibility risk.
- `ObsidianWriterAgent`: writes an Obsidian-style research vault.
- `ExperimentAgent`: selects audited papers for smoke tests and records run outcomes.
- `ReviewAgent`: checks citation support, metric support, and conclusion boundaries.

## Quick Start

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Initialize a research workspace:

```bash
research-repo init --topic "selective context forgetting in LLM inference"
```

Register a paper candidate:

```bash
research-repo add-paper \
  --title "Example Paper" \
  --url "https://arxiv.org/abs/example" \
  --code-url "https://github.com/example/project" \
  --method-type "benchmark" \
  --relevance 4
```

Audit, rank, and generate notes:

```bash
research-repo audit-paper --paper-id example-paper
research-repo rank-papers
research-repo select-experiments --top-k 3
research-repo write-vault
research-repo review
```

The CLI writes JSON artifacts under `artifacts/` and Obsidian-compatible markdown under `vault/`.

## Current Implementation Status

Implemented:

- JSON artifact schemas for briefs, paper candidates, audits, rankings, experiments, runs, and review records.
- Minimal CLI for `init`, `plan`, `add-paper`, `audit-paper`, `rank-papers`, `write-vault`, `select-experiments`, `run-smoke`, and `review`.
- Obsidian vault generation with index, topic map, paper notes, review notes, experiment notes, and run logs.
- Smoke-test selection after paper audit, not before.

Legacy:

- `research-repro-agent` still runs the earlier single-report demo.
- `scripts/run_demo.sh` is kept during migration.

## Documentation

- [docs/architecture.md](docs/architecture.md): system architecture.
- [docs/autoresearch_loop.md](docs/autoresearch_loop.md): staged loop and state transitions.
- [docs/obsidian_vault_spec.md](docs/obsidian_vault_spec.md): vault layout and note templates.
- [program.md](program.md): human-authored research program and agent rules.
