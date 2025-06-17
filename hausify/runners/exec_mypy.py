import subprocess
from pathlib import Path
from typing import Callable

from hausify.util.search import find_parent_configs

_configs = [
    "mypy.ini",
    ".mypy.ini",
    "pyproject.toml",
    "setup.cfg",
]


def exec_mypy(
    root: Path,
    files: list[Path],
    exec_cmd: Callable = subprocess.run,
) -> str:
    pyfiles = [f for f in files if f.suffix in (".py", ".pyi")]
    if not pyfiles:
        return ""

    iterations = find_parent_configs(root, pyfiles, _configs)
    all_errors = []
    for config, fileset in iterations.items():
        if len(fileset) == 0:
            continue

        result = _run_mypy_on_set(
            fileset=fileset,
            config=config,
            exec_cmd=exec_cmd,
        )

        if result != "":
            all_errors.append(f"(using config {config}):\n{result}")

    return "\n".join(all_errors)


def _run_mypy_on_set(
    fileset: list[Path],
    config: Path,
    exec_cmd: Callable = subprocess.run,
) -> str:
    """Run mypy on a set of files with a specific config."""

    cmd = [
        "mypy",
        "--show-error-codes",
    ]
    if config.is_file():
        cmd.append(f"--config-file={str(config)}")

    cmd.extend([str(f) for f in fileset])
    try:
        exec_cmd(
            cmd,
            check=True,
            text=True,
            capture_output=True,
        )
        return ""
    except subprocess.CalledProcessError as e:
        return e.stderr
