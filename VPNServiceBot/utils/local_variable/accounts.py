from utils.storage.storage import load_from_json

accounts = load_from_json("utils/storage/account.json")


def get_account():
    account = list(accounts['free'][0])
    accounts['free'].remove(accounts['free'][0])
    accounts['busy'].append(account)
    return account
