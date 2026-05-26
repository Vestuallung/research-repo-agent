# JSON Artifact Contract

AutoResearch artifacts are JSON files with a stable envelope. The envelope makes Agent output reviewable across stages and prevents bare JSON from losing version, producer, and status information.

## Envelope

Every new artifact uses this top-level shape:

```json
{
  "schema_version": "autoresearch.v0",
  "artifact_type": "paper_audit",
  "artifact_id": "sinktrack",
  "created_at": "2026-05-26T00:00:00Z",
  "updated_at": "2026-05-26T00:00:00Z",
  "producer": "PaperAuditAgent",
  "status": "audited",
  "data": {}
}
```

## Required Envelope Fields

- `schema_version`: fixed to `autoresearch.v0`.
- `artifact_type`: one of the schema-backed artifact types.
- `artifact_id`: slug identifier, not a file path.
- `created_at`: first write timestamp.
- `updated_at`: latest write timestamp.
- `producer`: Agent or component that produced the artifact.
- `status`: controlled lifecycle status.
- `data`: artifact-specific payload.

## Status Values

Allowed statuses:

- `draft`
- `candidate`
- `audited`
- `selected`
- `planned`
- `completed`
- `failed`
- `blocked`
- `needs_review`
- `checked`

## Artifact Types

- `research_brief`
- `paper_candidate`
- `paper_audit`
- `paper_priority_list`
- `selected_experiments`
- `experiment_task`
- `experiment_log`
- `review_record`

## Score Rules

Scores such as `topic_relevance`, `evidence_quality`, `code_availability`, and `reproducibility_value` use integers from `0` to `5`.

`priority` is a floating-point value because it is computed from weighted signals.

## Cross-Artifact References

Artifacts should reference each other by stable IDs:

- paper references use `paper_id`;
- experiment references use `experiment_id`;
- run references use `run_id`;
- review references use `review_id`.

File paths should not be used as primary identifiers.

## Schema Files

Schema files live in `schemas/`:

- `research_brief.schema.json`
- `paper_candidate.schema.json`
- `paper_audit.schema.json`
- `paper_priority_list.schema.json`
- `experiment_task.schema.json`
- `experiment_log.schema.json`
- `review_record.schema.json`
- `run_record.schema.json`

The Python implementation performs lightweight envelope checks and keeps compatibility with legacy bare JSON. Full JSON Schema validation can be added later without changing the artifact contract.
