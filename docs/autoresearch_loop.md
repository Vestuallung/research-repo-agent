# AutoResearch Loop

This project adapts AutoResearch-style control to literature-driven research.

## 1. Initialize

Input:

- topic;
- optional goal;
- optional exclusion scope;
- optional keywords.

Output:

- `artifacts/briefs/current.json`;
- initial vault pages.

## 2. Plan

The `DirectionAgent` expands the topic into a scoped research brief:

- research questions;
- keywords;
- likely method families;
- success criteria;
- exclusion rules.

Output:

- `artifacts/briefs/plan.md`.

## 3. Register Papers

The `LiteratureAgent` registers candidate papers. The first version accepts manually supplied metadata.

Output:

- `artifacts/papers/{paper_id}.json`.

## 4. Audit Papers

The `PaperAuditAgent` checks claims, evidence, code availability, reproducibility, and limitations.

Output:

- `artifacts/audits/{paper_id}.json`.

## 5. Rank And Select Experiments

The `ExperimentAgent` ranks audited papers and selects a small set for smoke tests.

Output:

- `artifacts/rankings/paper_priority.json`;
- `artifacts/rankings/selected_experiments.json`.

## 6. Write Vault

The `ObsidianWriterAgent` creates or updates an Obsidian-compatible vault.

Output:

- `vault/总索引.md`;
- `vault/主题地图.md`;
- `vault/论文总表.md`;
- `vault/papers/*.md`;
- `vault/reviews/*.md`;
- `vault/experiments/*.md`.

## 7. Run Smoke Tests

Smoke tests only target selected papers. A smoke test should verify a minimal execution surface:

- repository exists or can be referenced;
- dependency manifest is identifiable;
- entrypoint or official demo command is identifiable;
- failure type can be recorded if execution is not possible.

Output:

- `artifacts/experiments/{paper_id}.json`;
- `artifacts/experiments/{paper_id}-smoke-planned.json`;
- `vault/logs/{paper_id}-smoke-planned.md`.

The experiment artifact is a normalized `ExperimentLog`, not a free-form summary. It records environment, command spec, exit code, stdout/stderr summaries, failure type, and review notes.

## 8. Review

The `ReviewAgent` checks whether the vault and experiment outputs preserve traceability.

Output:

- `artifacts/reviews/review.json`;
- `vault/reviews/framework-review.md`.

## 9. Iterate

Failures should feed back into the next cycle:

- missing code link -> update candidate metadata;
- weak evidence -> downgrade priority;
- broken smoke test -> record failure type;
- unsupported draft claim -> convert to blocking question.
