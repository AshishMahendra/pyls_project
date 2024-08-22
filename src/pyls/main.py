import argparse
import json
import os
import time


def human_readable_size(size):
    """Converts a file size in bytes to a human-readable format."""
    suffixes = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while size >= 1024 and i < len(suffixes) - 1:
        size /= 1024.0
        i += 1
    return f"{size:.1f} {suffixes[i]}"


def find_item_by_path(contents, path):
    keys = path.strip("/").split("/") if path else []
    sub_contents = contents
    try:
        for key in keys:
            if key == "." or key == "":
                continue  # Skip the '.' and empty path components
            sub_contents = sub_contents["contents"]
            sub_contents = next(item for item in sub_contents if item["name"] == key)
        return sub_contents
    except StopIteration:
        raise KeyError(f"cannot access '{path}': No such file or directory")


def list_directory(
    contents,
    path,
    detailed=False,
    all_files=False,
    reverse=False,
    sort_by_time=False,
    filter_option=None,
    human_readable=False,
):
    try:
        sub_contents = find_item_by_path(contents, path)
        items = (
            sub_contents["contents"] if "contents" in sub_contents else [sub_contents]
        )
        if sort_by_time:
            items = sorted(items, key=lambda x: x["time_modified"], reverse=reverse)
        else:
            items = sorted(items, key=lambda x: x["name"], reverse=reverse)
    except KeyError as e:
        print(e)
        return

    results = []
    for item in items:
        if not all_files and item["name"].startswith("."):
            continue
        if filter_option == "file" and "contents" in item:
            continue
        if filter_option == "dir" and "contents" not in item:
            continue
        if detailed:
            mod_time = time.strftime(
                "%b %d %H:%M", time.localtime(item["time_modified"])
            )
            size = (
                human_readable_size(item["size"])
                if human_readable
                else str(item["size"])
            )
            result = f"{item['permissions']} {size.rjust(10)} {mod_time} {item['name']}"
        else:
            result = item["name"]
        results.append(result)

    if detailed:
        for result in results:
            print(result)
    else:
        print(" ".join(results))


class CustomArgParse(argparse.ArgumentParser):
    def error(self, message):
        if "invalid choice" in message and "--filter" in message:
            option = message.split("'")[1]
            self.exit(
                2,
                f"error: '{option}' is not a valid filter criteria. Available filters are 'dir' and 'file'\n",
            )
        else:
            super().error(message)


def parse_arguments():
    parser = CustomArgParse(
        description="Mimic ls command on a structured JSON directory.", add_help=False
    )
    parser.add_argument(
        "-h",
        "--human-readable",
        action="store_true",
        help="Display file sizes in human-readable format",
    )
    parser.add_argument(
        "-?",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit",
    )
    parser.add_argument(
        "path", nargs="?", default="", help="Path to list inside the JSON structure"
    )
    parser.add_argument("-l", "--long", action="store_true", help="Long listing format")
    parser.add_argument(
        "-A",
        "--all",
        action="store_true",
        help="Include directory entries whose names begin with a dot (.)",
    )
    parser.add_argument(
        "-r", "--reverse", action="store_true", help="Reverse the order of the sort"
    )
    parser.add_argument(
        "-t",
        "--time",
        action="store_true",
        help="Sort by modification time, oldest first",
    )
    parser.add_argument(
        "--filter",
        choices=["file", "dir"],
        help="Filter output to show only files or directories",
    )
    parser.add_argument(
        "--json-file",
        default="data/structure.json",
        help="Path to the JSON file containing the directory structure",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    json_file_path = args.json_file
    if not os.path.exists(json_file_path):
        print(f"Error: The file {json_file_path} does not exist.")
        return

    try:
        with open(json_file_path, "r") as file:
            data = json.load(file)
            list_directory(
                data,
                args.path,
                args.long,
                args.all,
                args.reverse,
                args.time,
                args.filter,
                args.human_readable,
            )
    except FileNotFoundError:
        print(f"Error: The file {json_file_path} does not exist.")
    except json.JSONDecodeError:
        print("Error: The file does not contain valid JSON.")


if __name__ == "__main__":
    main()
