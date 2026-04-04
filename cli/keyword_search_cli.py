import argparse
from cli.lib import DATA_DIR_PATH
from cli.lib.commands import build_command, search_command


file_path = DATA_DIR_PATH

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    build_parser = subparsers.add_parser("build", help="Build and save movies cache")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            # print the search query here
            print(f"Searching for: {args.query}")
            result = search_command(query=args.query, file_path=file_path, limit=10)
            
            sorted_result = sorted(result, key=lambda x:x["id"])

            for index, r in enumerate(sorted_result):
                print(f"{index + 1}. {r["title"]}")
            pass
        case "build":
            build_command()
            pass
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()

