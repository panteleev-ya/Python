import json


# Читаем из JSON
def load_from_json(path):
    with open(path) as json_file:
        data = json.load(json_file)
    return data


# Записываем в JSON
def store_json(path, data):
    with open(path, "w") as outfile:
        json.dump(data, outfile)


storage = load_from_json("utils/storage/storage.json")
