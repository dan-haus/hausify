from hausify.args import parse_args
from hausify.filesystem import SourceTree


def main():
    args = parse_args()
    print("ARGS:", args)

    tree = SourceTree(
        args.rootdir,
        args.files,
        args.exclude_dir,
    )
    print("SourceTree initialized.")
    print("root:", tree.rootdir)
    for _ in tree.source_files[:20]:
        print("\t", _)


if __name__ == "__main__":
    main()
