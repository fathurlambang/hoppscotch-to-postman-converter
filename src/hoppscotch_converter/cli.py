import argparse
import os
import sys

from .converter import convert_hoppscotch_to_postman_collection_v21, convert_hoppscotch_env_to_postman_env


def resolve_path(path):
    return os.path.abspath(os.path.expanduser(path))


def main():
    parser = argparse.ArgumentParser(
        prog="hoppscotch-converter",
        description="Convert Hoppscotch exports to Postman v2.1 format"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Collection converter
    collection_parser = subparsers.add_parser("collection", help="Convert Hoppscotch collection to Postman v2.1")
    collection_parser.add_argument("path", help="Hoppscotch JSON file or directory containing JSON files")
    collection_parser.add_argument("-o", "--output-dir", help="Output directory (default: current directory)")
    collection_parser.add_argument("-f", "--filter", help="Filter files by name pattern (e.g. 'Login' or '*.json')")

    # Environment converter
    env_parser = subparsers.add_parser("env", help="Convert Hoppscotch environment to Postman")
    env_parser.add_argument("path", nargs="?", help="Hoppscotch JSON file or directory containing JSON files")
    env_parser.add_argument("-o", "--output-dir", help="Output directory (default: current directory)")
    env_parser.add_argument("-f", "--filter", help="Filter files by name pattern (e.g. 'Local' or '*.json')")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    target_path = resolve_path(args.path) if args.path else None
    output_dir = resolve_path(args.output_dir) if args.output_dir else os.getcwd()

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    if args.command == "collection":
        if not target_path or not os.path.exists(target_path):
            print(f"Error: Path '{args.path}' not found")
            sys.exit(1)

        files = []
        if os.path.isfile(target_path):
            files = [target_path]
        elif os.path.isdir(target_path):
            files = [
                os.path.join(target_path, f)
                for f in sorted(os.listdir(target_path))
                if f.endswith(".json") and (not args.filter or args.filter in f)
            ]

        if not files:
            print(f"No JSON files found in '{args.path}'")
            sys.exit(1)

        for file in files:
            convert_hoppscotch_to_postman_collection_v21(file, output_dir=output_dir)

    elif args.command == "env":
        if not target_path or not os.path.exists(target_path):
            print(f"Error: Path '{args.path}' not found")
            sys.exit(1)

        files = []
        if os.path.isfile(target_path):
            files = [target_path]
        elif os.path.isdir(target_path):
            files = [
                os.path.join(target_path, f)
                for f in sorted(os.listdir(target_path))
                if f.endswith(".json") and (not args.filter or args.filter in f)
            ]

        if not files:
            print(f"No JSON files found in '{args.path}'")
            sys.exit(1)

        for file in files:
            convert_hoppscotch_env_to_postman_env(file, output_dir=output_dir)


if __name__ == "__main__":
    main()
