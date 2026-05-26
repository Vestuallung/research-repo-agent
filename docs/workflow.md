# Workflow

User input:

- Paper PDF, arXiv page, or a structured paper evaluation JSON.
- GitHub repository or local research code directory.

Step 1: Paper Agent

- Extracts metadata, paper type, primary claims, support scores, red flags, and blocking questions.
- Separates quality score from interest score so that exciting but weak papers are not over-trusted.

Step 2: Repo Agent

- Scans files.
- Detects dependency manifests such as `pyproject.toml` or `requirements.txt`.
- Detects entrypoint candidates such as `train.py`, `eval.py`, `main.py`, and scripts.
- Detects configs, tests, and example data files.

Step 3: Planner Agent

- Maps paper claims to repository signals.
- Assigns a reproduction risk level.
- Builds setup steps, smoke tests, and a minimal reproduction task list.

Step 4: Reporter

- Produces a markdown report for lab notes, GitHub issues, or course research logs.

Future Step: Debugger Agent

- Reads terminal logs.
- Classifies dependency, path, data, config, and runtime errors.
- Suggests patches or issue-style questions for the original repository.
