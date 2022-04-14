import json


# Reading JSON file
def load_from_json(path):
    with open(path) as json_file:
        data = json.load(json_file)
    return data


# Writing JSON file
def store_json(path, data):
    with open(path, "w") as outfile:
        json.dump(data, outfile)
