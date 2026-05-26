# Architecture

Research Repro Agent is an AutoResearch-style framework for automated research auditing. The system decomposes research work into staged, reviewable artifacts instead of producing one opaque final answer.

## Design Goal

The framework should support this loop:

```text
user topic
  -> DirectionAgent
  -> LiteratureAgent
  -> PaperAuditAgent
  -> candidate ranking
  -> ObsidianWriterAgent
  -> ExperimentAgent smoke tests on selected papers
  -> ReviewAgent
  -> report / vault / experiment log
```

The key rule is that experiment smoke tests happen after paper audit and ranking. The system should not spend effort running every paper repository.

## Agents

### MainAgent

Coordinates stage order, artifact paths, and review boundaries. It should not invent paper claims or experiment results.

### DirectionAgent

Creates a `ResearchBrief` from a user topic. It defines scope, keywords, exclusions, research questions, and success criteria.

### LiteratureAgent

Registers `PaperCandidate` records. In the first implementation, it accepts manually supplied URLs and metadata. Later versions can add search backends.

### PaperAuditAgent

Creates `PaperAudit` records. It reviews:

- main claims;
- evidence quality;
- code availability;
- reproducibility value;
- method type;
- limitations;
- blocking questions.

### ObsidianWriterAgent

Generates a markdown vault with wikilinks. It writes index pages, paper cards, review notes, experiment notes, and logs.

### ExperimentAgent

Ranks audited papers, selects candidates for smoke testing, proposes commands, records outcomes, and classifies failures. It does not default to heavy training or benchmark runs.

### ReviewAgent

Checks final artifacts for citation support, metric support, conclusion boundaries, and unresolved questions.

## Artifact Model

Artifacts are stored as JSON and markdown files.

```text
artifacts/
  briefs/
  papers/
  audits/
  rankings/
  experiments/
  reviews/
vault/
  总索引.md
  主题地图.md
  调研方向.md
  论文总表.md
  gaps.md
  papers/
  reviews/
  experiments/
  logs/
```

Core JSON models:

- `ResearchBrief`
- `PaperCandidate`
- `PaperAudit`
- `PaperPriorityScore`
- `ObsidianNotePlan`
- `ExperimentTask`
- `RunRecord`
- `ReviewRecord`

New JSON artifacts use a versioned envelope with `schema_version`, `artifact_type`, `artifact_id`, timestamps, `producer`, `status`, and `data`. The contract is documented in `docs/json_artifact_contract.md`.

## Candidate Ranking

Smoke-test priority is computed after paper audits.

```text
priority =
  0.30 * topic_relevance
+ 0.25 * reproducibility_value
+ 0.20 * code_availability
+ 0.15 * evidence_quality
+ 0.10 * method_diversity_bonus
- risk_penalty
```

Selection rules:

- papers without code links are skipped by default;
- papers with high risk penalties can be skipped even if relevant;
- top-k should cover diverse method types when possible;
- every selected or skipped paper gets an explicit reason.

## CLI Surface

Planned command surface:

```bash
research-repo init --topic "..."
research-repo plan
research-repo add-paper --url ...
research-repo audit-paper --paper-id ...
research-repo rank-papers
research-repo write-vault
research-repo select-experiments --top-k 3
research-repo run-smoke --selected
research-repo review
```

This first implementation uses local JSON and markdown only.

## Safety Rules

- Agent text starts as `draft`.
- Paper conclusions must trace back to `PaperAudit`.
- Experiment conclusions must trace back to normalized `ExperimentLog` artifacts.
- Smoke tests should verify minimal execution surfaces only.
- Failures are recorded as `Pivot/Refine` information.
- Final reports must distinguish paper claims, Agent inference, experiment observation, and review conclusion.
