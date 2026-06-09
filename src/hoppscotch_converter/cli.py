import argparse
import json
import os
import sys

from .converter import convert_hoppscotch_to_postman_collection_v21, convert_hoppscotch_env_to_postman_env


def resolve_path(path):
    return os.path.abspath(os.path.expanduser(path))


def is_hoppscotch_collection(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return "folders" in data or "requests" in data
    except (json.JSONDecodeError, KeyError):
        return False


def is_hoppscotch_env(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return "variables" in data and "folders" not in data and "requests" not in data
    except (json.JSONDecodeError, KeyError):
        return False


def process_path(target_path, output_dir, file_filter=None, mode=None):
    files = []
    if os.path.isfile(target_path):
        files = [target_path]
    elif os.path.isdir(target_path):
        files = [
            os.path.join(target_path, f)
            for f in sorted(os.listdir(target_path))
            if f.endswith(".json") and (not file_filter or file_filter in f)
        ]

    if not files:
        print(f"No JSON files found in '{target_path}'")
        sys.exit(1)

    for filepath in files:
        if mode == "env" or (mode is None and is_hoppscotch_env(filepath)):
            convert_hoppscotch_env_to_postman_env(filepath, output_dir=output_dir)
        elif mode == "collection" or (mode is None and is_hoppscotch_collection(filepath)):
            convert_hoppscotch_to_postman_collection_v21(filepath, output_dir=output_dir)
        else:
            print(f"Skipped '{filepath}': not a recognized Hoppscotch file")


def main():
    parser = argparse.ArgumentParser(
        prog="hoppscotch-converter",
        description="Convert Hoppscotch exports to Postman v2.1 format"
    )

    parser.add_argument("path", nargs="?", help="Hoppscotch JSON file or directory")
    parser.add_argument("-o", "--output-dir", help="Output directory (default: current directory)")
    parser.add_argument("-f", "--filter", help="Filter files by name pattern")
    parser.add_argument("-t", "--type", choices=["collection", "env"], help="Force file type (collection or env)")

    args = parser.parse_args()

    if not args.path:
        parser.print_help()
        sys.exit(1)

    target_path = resolve_path(args.path)
    output_dir = resolve_path(args.output_dir) if args.output_dir else os.getcwd()

    if not os.path.exists(target_path):
        print(f"Error: Path '{args.path}' not found")
        sys.exit(1)

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    process_path(target_path, output_dir, file_filter=args.filter, mode=args.type)


if __name__ == "__main__":
    main()
