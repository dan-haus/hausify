import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Hausify: A python linter/formatter for Haus."
    )

    parser.add_argument(
        "--rootdir",
        help="The root directory of the project (do not recurse above).",
        default=".",
        type=str,
    )

    parser.add_argument(
        "--tool",
        help="The tool to run (e.g. black, isort, flake8, mypy).",
        choices=[
            "all",
            "black",
            "isort",
            "flake8",
            "mypy",
        ],
        default="all",
        type=str,
    )

    parser.add_argument(
        "--exclude_dir",
        help="Directories to exclude from linting/formatting.",
        default=[],
        metavar="DIR_REGEX",
        action="append",
        type=str,
    )

    parser.add_argument(
        "files",
        help=(
            "The files to lint/format. If not provided, all python (.py, .pyi) "
            "files in the root directory will be processed."
        ),
        nargs="*",
        metavar="FILEPATH(S)",
        type=str,
    )

    return parser.parse_args()
