from collections import defaultdict
import os
import pickle
from cli.lib import CACHE_DIR, DOCMAP_PATH, INDEX_PATH, has_matching_tokens, load_data, load_stop_words, stop_word_filter, tokenize_text

def search_command(query, file_path, limit = 5):
    data = load_data(file_path=file_path)
    stop_words = load_stop_words()
    inverted_index = InvertedIndex()
    inverted_index.load()

    # print(index)

    # movies = data["movies"]

    result = []

    for token in tokenize_text(query):
        doc_ids =inverted_index.get_documents(token)

        for doc_id in doc_ids:
            movie = inverted_index.docmap.get(doc_id)
            movie_title = movie["title"]
            result.append({"id": doc_id, "title": movie_title})
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

    def load(self):
        is_index_file = os.path.isfile(INDEX_PATH)
        is_docmap_file = os.path.isfile(DOCMAP_PATH)
        if(not is_index_file):
            print("Index File not found")
            return

        if(not is_docmap_file):
            print("DOCMAP File not found")
            return

        with open(INDEX_PATH, "rb") as file:
            self.index =  pickle.load(file)

        with open(DOCMAP_PATH, "rb") as file:
            self.docmap =  pickle.load(file)
       

def build_command():
    inverted_index = InvertedIndex()
    inverted_index.build()
    inverted_index.save()
    # docs = inverted_index.get_documents("merida")