# Reproduction Agent Report: H-Neurons: On the Existence, Impact, and Origin of Hallucination-Associated Neurons in LLMs

## Agent Flow

Paper Agent extracted claims, support levels, weaknesses, and red flags.
Repo Agent scanned local files to locate entrypoints, configs, tests, and dependency manifests.
Planner Agent converted both signals into a minimal reproduction checklist.

## Paper Signals

- Primary type: `empirical_method`
- Tags: `llm, safety_alignment`
- Final score: `42.25`
- Risk level: `high`

## Claims

- C1: support=1/2; A very sparse subset of FFN neurons can robustly predict hallucinations across models and settings.
- C2: support=1/2; These neurons causally control a broader over-compliance tendency, not just factual hallucination.
- C3: support=1/2; These neurons originate in pretraining and are largely preserved through instruction tuning.

## Repository Signals

- Root: `.`
- Files scanned: `38`
- Entrypoints: `scripts/run_demo.sh, src/research_repro_agent/cli.py`
- Dependencies: `pyproject.toml, requirements.txt`
- Configs: `examples/hneurons_evaluation.json, pyproject.toml`
- Tests: `none`

## Setup Steps

- Install dependencies from pyproject.toml, requirements.txt.
- Inspect config files: examples/hneurons_evaluation.json, pyproject.toml.

## Smoke Tests

- Try a minimal dry run through scripts/run_demo.sh.

## Reproduction Tasks

- Map each primary claim to the exact script, dataset, and metric needed for verification.
- Reproduce one table or figure before attempting full-scale experiments.
- Record missing seeds, run counts, compute setup, and judge prompts as blocking gaps.

## Agent Notes

- Paper type: empirical_method; tags: llm, safety_alignment.
- Detected 38 repository files, 2 candidate entrypoints.
- Risk from paper evaluation: The core method description contains a major internal contradiction about label direction and neuron interpretation.
- Risk from paper evaluation: The causal claim is weakly isolated because key matched perturbation controls are absent.
- Risk from paper evaluation: Reproducibility is limited by missing code path, seeds, run counts, uncertainty reporting, compute disclosure, and incomplete judge specification.

## Blocking Questions

- What exact label direction was used in the logistic probe?
- Do the intervention results persist under random matched neurons, negative-weight neurons, or alternative sparse subsets?
- How stable are selected neurons across seeds, splits, and answer-span labeling methods?
- How large is benchmark contamination or memorization risk on the public QA sets used?
- How sensitive are judge-based results to the GPT-4o prompt and rubric?
