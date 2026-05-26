# Obsidian Vault Specification

The generated vault is a reviewable research workspace. It should be readable as plain markdown and usable inside Obsidian.

## Directory Layout

```text
vault/
  总索引.md
  主题地图.md
  调研方向.md
  论文总表.md
  gaps.md
  papers/
    paper-id.md
  reviews/
    paper-id-review.md
    framework-review.md
  experiments/
    paper-id-smoke.md
  logs/
    paper-id-run.md
```

## Wikilink Rules

- Use Obsidian wikilinks for internal notes.
- Paper notes should link back to `[[论文总表]]`.
- Review notes should link to their paper note.
- Experiment notes should link to both paper and review notes.

## Paper Note Template

Each paper note should include:

```markdown
---
type: paper
paper_id: example-paper
status: draft
---

# Paper Title

## Metadata

## Main Claims

## Evidence Map

## Method Summary

## Experiment Setup

## Reproducibility Notes

## Smoke Test Priority

## Limitations

## Related Notes
```

## Review Note Template

Each review note should include:

```markdown
---
type: paper_review
paper_id: example-paper
status: draft
---

# Review: Paper Title

## Audit Summary

## Citation Check

## Metric Check

## Boundary Check

## Blocking Questions
```

## Experiment Note Template

Each experiment note should include:

```markdown
---
type: smoke_test
paper_id: example-paper
status: planned
---

# Smoke Test: Paper Title

## Selection Reason

## Repository

## Proposed Command

## Result

## Failure Type
```

## Log Note Template

Each normalized run log should include:

```markdown
# Run: paper-id-smoke-planned

- experiment_id: paper-id-smoke
- paper_id: paper-id
- repo_url: https://github.com/example/project
- mode: planned
- command: inspect repository metadata
- status: planned
- failure_type: not_run
- review_result: planned_only

## stdout

## Review Notes
```

## Status Labels

- `draft`: generated but not reviewed.
- `needs_review`: plausible but not checked.
- `checked`: reviewed against source artifacts.
- `blocked`: cannot proceed because required evidence or code is missing.
- `final`: accepted for final report.
