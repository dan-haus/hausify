import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Hausify: A python linter/formatter for Haus."
    )

    parser.add_argument(
        "--rootdir",
        help="The root directory to start searching for config files.",
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
        "files",
        help="The files to lint/format. If not provided, all files in the root directory will be processed.",
        nargs="*",
        type=str,
    )

    return parser.parse_args()
