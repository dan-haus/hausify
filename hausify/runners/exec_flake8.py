import subprocess
from pathlib import Path
from typing import Callable

from hausify.util.search import find_parent_configs

_configs = [
    ".flake8",
    "setup.cfg",
    "tox.ini",
]


def exec_flake8(
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

        result = _run_flake8_on_set(
            fileset=fileset,
            config=config,
            exec_cmd=exec_cmd,
        )

        if result != "":
            all_errors.append(f"(using config {config}):\n{result}")

    return "\n".join(all_errors)


def _run_flake8_on_set(
    fileset: list[Path],
    config: Path,
    exec_cmd: Callable = subprocess.run,
) -> str:
    """Run flake8 on a set of files with a specific config."""

    cmd = [
        "flake8",
        "--color=always",
    ]
    if config.is_file():
        cmd.extend(["--config", str(config)])

    cmd.extend(str(f) for f in fileset)

    try:
        result = exec_cmd(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stdout + e.stderr
