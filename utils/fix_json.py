import json
from json_repair import repair_json

with open("./data/movies.json", "r", encoding="utf-8") as file:
    content = file.read()
    
    fixed_data = repair_json(content, return_objects=True)

    with open("./data/fixed_movies.json", "w") as json_file:
        json.dump(fixed_data, json_file)

