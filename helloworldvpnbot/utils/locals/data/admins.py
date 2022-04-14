from utils.locals.scripts.storage import load_from_json, store_json

# Admins information
# 'admins' -> list of usernames
# 'chat_id' -> admins telegram chat ID
admins = load_from_json("utils/storage/admins.json")

# Administrators telegram chat ID
admin_chat_id = admins['chat_id']


# Register new admin
def register_new_admin(username):
    admins['admins'].append(username)
    store_json("utils/storage/admins.json", admins)


# Check if user is admin
def is_admin(username):
    return username in admins['admins']
