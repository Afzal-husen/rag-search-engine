from collections import defaultdict
import os
import pickle
from cli.lib import CACHE_DIR, DOCMAP_PATH, INDEX_PATH, has_matching_tokens, load_data, load_stop_words, stop_word_filter, tokenize_text

def search_command(query, file_path, limit = 5):
    data = load_data(file_path=file_path)
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
        data = load_data()
        movies = data["movies"]

        # iterate over movies list
        # add to both index and docmap
        # concatenate title and description and pass it as text into __add_document
        for movie in movies:
            movie_id = movie["id"]
            self.__add_document(doc_id=movie_id, text=f"{movie["title"]} {movie["description"]}")
            self.docmap.setdefault(movie_id, movie)
        
    def save(self):
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(INDEX_PATH, "wb") as file:
            pickle.dump(self.index, file=file)

        with open(DOCMAP_PATH, "wb") as file:
            pickle.dump(self.docmap, file=file)

def build_command():
    inverted_index = InvertedIndex()
    inverted_index.build()
    inverted_index.save()
    docs = inverted_index.get_documents("merida")
    print(f"First document for token 'merida' = {docs[0]}")