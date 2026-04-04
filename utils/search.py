from utils import has_matching_tokens, load_data, load_stop_words, stop_word_filter, tokenize_text

def search(query, file_path, limit = 5):
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