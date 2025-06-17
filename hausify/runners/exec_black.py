import subprocess
from pathlib import Path
from typing import Callable

from hausify.util.python_import_finder import PythonImportFinder
from hausify.util.search import find_parent_configs

_configs = [
    "pyproject.toml",
]


def exec_black(
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

        result = _run_black_on_set(
            fileset=fileset,
            config=config,
            exec_cmd=exec_cmd,
        )

        if result != "":
            all_errors.append(f"(using config {config}):\n{result}")

    return "\n".join(all_errors)


def _run_black_on_set(
    fileset: list[Path],
    config: Path,
    exec_cmd: Callable = subprocess.run,
) -> str:
    """Run black on a set of files with a specific config."""
    results = []
    for filename in fileset:
        cmd = [
            "black",
            "--color",
        ]

        if config.is_file():
            cmd.extend(["--config", str(config)])

        finder = PythonImportFinder()
        finder.load_source_file(filename)
        format_ranges = finder.get_formatting_ranges()

        for start, end in format_ranges:
            cmd.extend(["--line-ranges", f"{start}-{end}"])

        cmd.append(str(filename))
        try:
            result = exec_cmd(
                cmd,
                check=True,
                text=True,
                capture_output=True,
            )
            if result.stdout:
                results.append(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            return e.stdout.strip() + "\n" + e.stderr.strip()

    if len(results) > 0:
        print(f"Formatted {len(results)} files with black.")
        print("\n".join(results))

    return ""
