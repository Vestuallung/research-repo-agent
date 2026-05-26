from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from autoresearch.schemas.models import ARTIFACT_TYPES, SCHEMA_VERSION, STATUSES, ArtifactEnvelope


ARTIFACT_DIRS = [
    "artifacts/briefs",
    "artifacts/papers",
    "artifacts/audits",
    "artifacts/rankings",
    "artifacts/experiments",
    "artifacts/reviews",
    "vault/papers",
    "vault/reviews",
    "vault/experiments",
    "vault/logs",
]


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"https?://", "", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text or "untitled"


def ensure_workspace(root: Path) -> None:
    for rel in ARTIFACT_DIRS:
        (root / rel).mkdir(parents=True, exist_ok=True)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_artifact(
    path: Path,
    *,
    artifact_type: str,
    artifact_id: str,
    producer: str,
    status: str,
    data: dict[str, Any],
) -> ArtifactEnvelope:
    if artifact_type not in ARTIFACT_TYPES:
        raise ValueError(f"unknown artifact_type: {artifact_type}")
    if status not in STATUSES:
        raise ValueError(f"unknown status: {status}")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", artifact_id):
        raise ValueError(f"artifact_id must be a slug: {artifact_id}")
    now = utc_now()
    existing = read_json(path) if path.exists() else None
    created_at = existing.get("created_at", now) if isinstance(existing, dict) else now
    envelope = ArtifactEnvelope(
        schema_version=SCHEMA_VERSION,
        artifact_type=artifact_type,
        artifact_id=artifact_id,
        created_at=created_at,
        updated_at=now,
        producer=producer,
        status=status,
        data=data,
    )
    write_json(path, envelope.to_dict())
    return envelope


def read_artifact(path: Path) -> dict[str, Any]:
    raw = read_json(path)
    if isinstance(raw, dict) and raw.get("schema_version") == SCHEMA_VERSION and "data" in raw:
        return raw["data"]
    return raw


def read_artifact_envelope(path: Path) -> dict[str, Any]:
    raw = read_json(path)
    if isinstance(raw, dict) and raw.get("schema_version") == SCHEMA_VERSION and "data" in raw:
        return raw
    return {
        "schema_version": "legacy",
        "artifact_type": "legacy",
        "artifact_id": path.stem,
        "producer": "legacy",
        "status": raw.get("status", "draft") if isinstance(raw, dict) else "draft",
        "data": raw,
    }


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def iter_json_files(path: Path) -> list[Path]:
    if not path.exists():
        return []
    return sorted(p for p in path.glob("*.json") if p.is_file())
