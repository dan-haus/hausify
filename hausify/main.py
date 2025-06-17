import sys
from subprocess import run as subprocess_run

from hausify.args import parse_args
from hausify.runners.exec_isort import exec_isort
from hausify.util.filesystem import SourceTree


def main():
    args = parse_args()

    tree = SourceTree(
        args.rootdir,
        args.files,
        args.exclude_dir,
    )

    should_exit = False

    if args.tool == "all" or args.tool == "isort":
        result = exec_isort(
            tree.rootdir,
            tree.source_files,
            exec_cmd=subprocess_run,
        )
        if result != "":
            print("ISORT ERRORS:")
            print(result)
            should_exit = True

    if should_exit:
        sys.exit(1)


if __name__ == "__main__":
    main()
