import argparse
import json
from shutil import move
import string

file_path = "./data/movies.json"


def load_data():
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            
            data:dict = json.load(file)

            return data
    except FileNotFoundError:
        print(f"Error: The file at path: {file_path} not found")
    except json.JSONDecodeError as e:
        print(f"Error: The file at path: {file_path} has invalid json format", e)

def text_preprocess(text:str):
    text = text.lower()
    translator = text.maketrans("", "", string.punctuation)
    return text.translate(translator)


def search(query, limit = 5):
    data = load_data()
    stop_words = load_stop_words()

    movies = data["movies"]

    result = []

    for movie in movies:
        tokenized_title: str = tokenize_text(movie["title"])
        tokenized_query: str = tokenize_text(query)

        filtered_title_tokens = stop_word_filter(tokens=tokenized_title, stop_words=stop_words)
        filtered_query_tokens = stop_word_filter(tokens=tokenized_query, stop_words=stop_words)
     
        if has_matching_tokens(query_tokens=filtered_query_tokens, title_tokens=filtered_title_tokens):
            result.append(movie)


        if len(result) >= limit:
            break
        
    return result
    
def tokenize_text(text:str):
    text = text_preprocess(text)
    tokenized_text = text.split()
    valid_tokens = []
    for token in tokenized_text:
        if token:
            valid_tokens.append(token)
    return valid_tokens

def has_matching_tokens(query_tokens: list[str], title_tokens: list[str]):
    for query_token in query_tokens:
        for title_token in title_tokens:
            if query_token in title_token:
                return True
    return False

def load_stop_words():
    with open("./data/stopwords.txt", "r", encoding="utf-8") as file:
        data = file.read()
        words_list = data.splitlines()
        return words_list

def stop_word_filter(tokens: list[str], stop_words: list[str]):
    clean_tokens = []
    for token in tokens:
        if token not in stop_words:
            clean_tokens.append(token)
    return clean_tokens
    


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
            result = search(args.query, 10)
            
            sorted_result = sorted(result, key=lambda x:x["id"])

            for index, r in enumerate(sorted_result):
                print(f"{index + 1}. {r["title"]}")
            pass
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()

