from utils.locals.scripts.storage import load_from_json, store_json

# Subscription options information
# 1) Prices list
# 2) Durations list
options = load_from_json("utils/storage/subscription_options.json")
prices = options['prices']
subscription_durations = options['durations']
