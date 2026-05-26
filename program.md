# Research Program

This file defines the human-authored research program for the autonomous research audit loop.

## Goal

Build an auditable research workflow that starts from a topic, discovers and reviews papers, writes an Obsidian-compatible research vault, selects high-value papers for smoke testing, and records reviewable conclusions.

## Agent Organization

The system uses specialized agents:

- `MainAgent`: owns stage order and artifact paths.
- `DirectionAgent`: converts a topic into a scoped research brief.
- `LiteratureAgent`: registers paper candidates and search metadata.
- `PaperAuditAgent`: evaluates claims, evidence, code availability, and reproducibility.
- `ObsidianWriterAgent`: writes markdown notes with wikilinks.
- `ExperimentAgent`: selects audited papers for smoke tests and records run outcomes.
- `ReviewAgent`: checks citations, metrics, unsupported claims, and conclusion boundaries.

## Rules

1. Claims must be extracted before summaries are written.
2. Paper audits must happen before experiment selection.
3. Smoke tests must only target papers selected after audit and ranking.
4. Agent-written text is `draft` until reviewed.
5. Experiment conclusions must point to `RunRecord` artifacts.
6. Final reports must distinguish paper claims, agent inference, experiment observation, and review conclusion.
7. Failed experiments must be recorded as information, not hidden.

## Default Loop

```text
init brief
  -> add paper candidates
  -> audit papers
  -> rank papers
  -> select experiments
  -> write vault
  -> record smoke tests
  -> review artifacts
```

## Smoke Test Policy

Smoke tests verify only the smallest meaningful execution surface:

- dependency discovery;
- entrypoint discovery;
- official demo command if obvious;
- import or help command if no demo exists;
- failure classification when execution cannot proceed.

Heavy training, long benchmark runs, and destructive commands are out of scope by default.
