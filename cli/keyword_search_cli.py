import argparse
from collections import defaultdict
from utils import tokenize_text, load_data
from utils.search import search
import pickle

file_path = "./data/movies.json"

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
            result = search(query=args.query, file_path=file_path, limit=10)
            
            sorted_result = sorted(result, key=lambda x:x["id"])

            for index, r in enumerate(sorted_result):
                print(f"{index + 1}. {r["title"]}")
            pass
        case "build":
            inverted_index = InvertedIndex()
            inverted_index.build()
            inverted_index.save()
            docs = inverted_index.get_documents("merida")
            print(f"First document for token 'merida' = {docs[0]}")
            pass
        case _:
            parser.print_help()


class InvertedIndex():
    def __init__(self):
        self.index = defaultdict(set) #dic mapping to set eg: "abc" -> {1, 2,3,4}
        self.docmap = defaultdict()

    def __add_document(self, doc_id, text):
        for token in tokenize_text(text):
            self.index[token].add(doc_id)

    def get_documents(self, term:str):
        term = term.lower()
        return list(self.index.get(term))

    def build(self):
        data = load_data(file_path=file_path)
        movies = data["movies"]

        # iterate over movies list
        # add to both index and docmap
        # concatenate title and description and pass it as text into __add_document
        for movie in movies:
            movie_id = movie["id"]
            self.__add_document(doc_id=movie_id, text=f"{movie["title"]} {movie["description"]}")
            self.docmap.setdefault(movie_id, movie)
        
    def save(self):
        with open("./cli/cache/index.pkl", "wb") as file:
            pickle.dump(self.index, file=file)

        with open("./cli/cache/docmap.pkl", "wb") as file:
            pickle.dump(self.docmap, file=file)

if __name__ == "__main__":
    main()

