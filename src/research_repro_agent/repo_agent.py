from __future__ import annotations

from pathlib import Path

from .models import RepoSignal


ENTRYPOINT_NAMES = {
    "cli.py",
    "main.py",
    "train.py",
    "eval.py",
    "evaluate.py",
    "run.py",
    "app.py",
}

DEPENDENCY_NAMES = {
    "requirements.txt",
    "pyproject.toml",
    "environment.yml",
    "setup.py",
    "package.json",
    "uv.lock",
}

CONFIG_SUFFIXES = {".yaml", ".yml", ".toml", ".json", ".ini"}
DATA_SUFFIXES = {".csv", ".jsonl", ".parquet", ".tsv"}


def scan_repo(root: str | Path) -> RepoSignal:
    base = Path(root).resolve()
    files = [
        str(path.relative_to(base))
        for path in base.rglob("*")
        if path.is_file() and ".git" not in path.parts
    ]
    files.sort()

    likely_entrypoints: list[str] = []
    config_files: list[str] = []
    dependency_files: list[str] = []
    data_files: list[str] = []
    test_files: list[str] = []

    for rel in files:
        path = Path(rel)
        name = path.name.lower()
        if name in ENTRYPOINT_NAMES or path.parts[:1] in [("scripts",), ("bin",)]:
            likely_entrypoints.append(rel)
        if name in DEPENDENCY_NAMES:
            dependency_files.append(rel)
        if path.suffix.lower() in CONFIG_SUFFIXES:
            config_files.append(rel)
        if path.suffix.lower() in DATA_SUFFIXES and "examples" in path.parts:
            data_files.append(rel)
        if name.startswith("test_") or "tests" in path.parts:
            test_files.append(rel)

    return RepoSignal(
        root=str(base),
        files=files,
        likely_entrypoints=likely_entrypoints,
        config_files=config_files,
        dependency_files=dependency_files,
        data_files=data_files,
        test_files=test_files,
    )
