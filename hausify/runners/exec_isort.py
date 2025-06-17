import subprocess
from pathlib import Path
from typing import Callable

from hausify.util.search import find_parent_configs

_configs = [
    ".isort.cfg",
    "pyproject.toml",
    "setup.cfg",
    "tox.ini",
]


def exec_isort(
    root: Path,
    files: list[Path],
    exec_cmd: Callable = subprocess.run,
) -> str:
    pyfiles = [f for f in files if f.suffix == ".py"]
    if not pyfiles:
        return ""

    iterations = find_parent_configs(root, pyfiles, _configs)
    all_errors = []
    for config, fileset in iterations.items():
        if len(fileset) == 0:
            continue

        result = _run_isort_on_set(
            fileset=fileset,
            config=config,
            exec_cmd=exec_cmd,
        )

        if result != "":
            all_errors.append(f"Error in {config}:\n{result}")

    return "\n".join(all_errors)


def _run_isort_on_set(
    fileset: list[Path],
    config: Path,
    exec_cmd: Callable = subprocess.run,
) -> str:
    """Run isort on a set of files with a specific config."""

    cmd = [
        "isort",
        "--color",
    ]
    if config.is_file():
        cmd.extend(["--settings-path", str(config)])

    cmd.extend(str(f) for f in fileset)

    try:
        result = exec_cmd(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr
