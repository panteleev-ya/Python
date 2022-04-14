from utils.locals.scripts.storage import load_from_json, store_json

# Subscription options information
# 1) Prices list
# 2) Durations list
options = load_from_json("utils/storage/subscription_options.json")

# Russian symbols makes me hardcode subscribe durations
hardcoded_subscribe_durations = {
    "30 дней": 30,
    "90 дней": 90,
}
options['durations'] = hardcoded_subscribe_durations
store_json("utils/storage/subscription_options.json", options)

prices = options['price']
subscription_durations = options['durations']
