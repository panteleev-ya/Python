from utils.locals.scripts.storage import load_from_json, store_json

# VPN service accounts info
accounts = load_from_json("utils/storage/accounts.json")


# Returns first 'free' account and makes it 'busy' after
def get_account():
    account = list(accounts['free'][0])
    accounts['free'].remove(accounts['free'][0])
    accounts['busy'].append(account)
    store_json("utils/storage/accounts.json", accounts)
    return account
