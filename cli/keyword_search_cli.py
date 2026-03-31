import argparse
import json

file_path = "./data/movies.json"

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            # print the search query here
            print(f"Searching for: {args.query}")
            result = load_data(args.query)
            
            sorted_result = sorted(result, key=lambda x:x["id"])

            truncated_result = sorted_result[:5]

            for index, r in enumerate(truncated_result):
                print(f"{index + 1}. {r["title"]}")
            pass
        case _:
            parser.print_help()




def load_data(query:str):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            
            data = json.load(file)
            movies = data["movies"]

            result = []

            for movie in movies:
                title: str = movie["title"]
                if query.lower() in title.lower():
                    result.append(movie)
                    
            return result
    except FileNotFoundError:
        print(f"Error: The file at path: {file_path} not found")
    except json.JSONDecodeError as e:
        print(f"Error: The file at path: {file_path} has invalid json format", e)


if __name__ == "__main__":
    main()