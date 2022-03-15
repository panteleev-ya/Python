from utils.storage.storage import load_from_json, store_json

admins = load_from_json("utils/storage/admins.json")


def register_new_admin(username):
    admins['admins'].append(username)
    store_json("utils/storage/admins.json", admins)
