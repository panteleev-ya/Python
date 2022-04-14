from utils.locals.scripts.storage import load_from_json, store_json

# Users information
users = load_from_json("utils/storage/users.json")


def save_users(new_users):
    store_json("utils/storage/users.json", new_users)
