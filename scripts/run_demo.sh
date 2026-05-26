#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PYTHONPATH=src python -m research_repro_agent.cli \
  --paper-eval examples/hneurons_evaluation.json \
  --repo . \
  --out examples/demo_reproduce_report.md
