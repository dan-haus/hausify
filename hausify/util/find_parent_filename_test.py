import pytest


def _build_test_file_structure(paths: list[tuple[str, str]], tmp_path):
    """
    Builds a test file structure based on the provided paths.
    Each tuple in the list contains a directory path and a file name.
    If the file name is an empty string, no file is created in that directory.
    """
    for dir, file in paths:
        curr_dir = tmp_path / dir
        curr_dir.mkdir(parents=True, exist_ok=True)
        if file != "":
            with open(curr_dir / file, "w") as f:
                f.write(f"This is a test file in {file}.")
    return tmp_path


def test_search_upward_for_parent_name_finds_same_directory_file(tmp_path):
    from hausify.util.find_parent_filename import search_upward_for_parent_name
    from pathlib import Path

    _build_test_file_structure(
        [
            ("above_root/root/dir1/dir2/", "file"),
            ("above_root/root/dir1/dir2/", "needle"),
        ],
        tmp_path,
    )

    found_path = search_upward_for_parent_name(
        filepath=tmp_path / Path("above_root/root/dir1/dir2/file"),
        parent_file="needle",
    )

    assert found_path == tmp_path / Path("above_root/root/dir1/dir2/needle")


def test_search_upward_for_parent_name_returns_none_if_parent_not_found(tmp_path):
    from hausify.util.find_parent_filename import search_upward_for_parent_name
    from pathlib import Path

    _build_test_file_structure(
        [
            ("above_root/root/dir1/dir2/", "file"),
        ],
        tmp_path,
    )

    found_path = search_upward_for_parent_name(
        filepath=tmp_path / Path("above_root/root/dir1/dir2/file"),
        parent_file="needle",
    )

    assert found_path is None


def test_search_upward_for_parent_name_does_not_find_sibling(tmp_path):
    from hausify.util.find_parent_filename import search_upward_for_parent_name
    from pathlib import Path

    _build_test_file_structure(
        [
            ("above_root/root/dir1/dir2/", "file"),
            ("above_root/root/dir1/", ""),
            ("above_root/root/dir1/dir3/", "needle"),
        ],
        tmp_path,
    )

    found_path = search_upward_for_parent_name(
        filepath=tmp_path / Path("above_root/root/dir1/dir2/file"),
        parent_file="needle",
        rootdir=tmp_path / Path("above_root/root"),
    )

    assert found_path is None


def test_search_upward_for_parent_name_finds_in_root(tmp_path):
    from hausify.util.find_parent_filename import search_upward_for_parent_name
    from pathlib import Path

    _build_test_file_structure(
        [
            ("above_root/root/dir1/dir2/", "file"),
            ("above_root/root/dir1/", ""),
            ("above_root/root/", "needle"),
        ],
        tmp_path,
    )

    found_path = search_upward_for_parent_name(
        filepath=tmp_path / Path("above_root/root/dir1/dir2/file"),
        parent_file="needle",
        rootdir=tmp_path / Path("above_root/root"),
    )

    assert found_path == tmp_path / Path("above_root/root/needle")


def test_search_upward_for_parent_name_does_not_find_above_root(tmp_path):
    from hausify.util.find_parent_filename import search_upward_for_parent_name
    from pathlib import Path

    _build_test_file_structure(
        [
            ("above_root/root/dir1/dir2/", "file"),
            ("above_root/root/dir1/", ""),
            ("above_root/", "needle"),
        ],
        tmp_path,
    )

    found_path = search_upward_for_parent_name(
        filepath=tmp_path / Path("above_root/root/dir1/dir2/file"),
        parent_file="needle",
        rootdir=tmp_path / Path("above_root/root"),
    )

    assert found_path is None


def test_search_upward_for_parent_name_does_not_finds_first_of(tmp_path):
    from hausify.util.find_parent_filename import search_upward_for_parent_name
    from pathlib import Path

    _build_test_file_structure(
        [
            ("above_root/root/dir1/dir2/", "file"),
            ("above_root/root/dir1/", "needle_a"),
            ("above_root/root/dir1/", "needle_b"),
        ],
        tmp_path,
    )

    found_path = search_upward_for_parent_name(
        filepath=tmp_path / Path("above_root/root/dir1/dir2/file"),
        parent_file=["not_present", "needle_b", "needle_a"],
        rootdir=tmp_path / Path("above_root/root"),
    )

    assert found_path == tmp_path / Path("above_root/root/dir1/needle_b")
