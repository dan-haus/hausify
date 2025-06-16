from typing import Optional
import os
from pathlib import Path


def get_git_root() -> Path:
    """Get the root directory of the git repository."""
    try:
        return Path(os.popen("git rev-parse --show-toplevel").read().strip())
    except Exception as e:
        print(f"Error getting git root: {e}")
        return Path.cwd()


def search_upward_for_parent_name(
    filepath: Path,
    parent_file: str,
    rootdir: Optional[Path] = None,
) -> Optional[Path]:
    """Searches upward from the given filename to find a file with the parent name.

    Includes the current directory and the root directory in the search.
    Args:
        rootdir (str): The root directory to stop searching at.
        filename (str): The starting file from which to begin the search.
        parent_name (str): The name of the parent file to search for.
    Returns:
        str: The path to the parent file if found, otherwise an empty string.
    """
    if rootdir is None:
        rootdir = get_git_root()

    if not filepath.is_absolute():
        filepath = rootdir / filepath

    current_dir = filepath.absolute().parent
    depth = 0

    while depth < 50:  # Limit the search depth to prevent infinite loops
        parent_path = current_dir / parent_file
        print(parent_path)

        if parent_path.is_file():
            return parent_path

        if current_dir == rootdir:
            break

        current_dir = current_dir.parent
        if not current_dir.exists():
            break
        depth += 1

    return None
