import json
import string
from nltk.stem import PorterStemmer

def load_data(file_path:str):
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

    
def stem_word(token:str):
    stemmer = PorterStemmer()
    stem_word = stemmer.stem(token)
    return stem_word

def stop_word_filter(tokens: list[str], stop_words: list[str]):
    clean_tokens = []
    for token in tokens:
        if token not in stop_words:
            stem_token = stem_word(token)
            clean_tokens.append(stem_token)
    return clean_tokens


