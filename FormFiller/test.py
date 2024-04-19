import requests

form_url_base = "https://docs.google.com/forms/d/e/1FAIpQLSfGxx6rqHDIjujNeSCr-NBLxry_ZmnVT6s5oWvFmu_-y0sQMQ"
form_response_url = f"{form_url_base}/formResponse"
form_view_url = f"{form_url_base}/viewForm"

owner_mapper = {
}

field_mapper = {
    "cost": "entry.1441644747",
    "category": "entry.767764842",
    "card_number": "entry.1727782915",
    "bank": "entry.412290270",
    "owner": "entry.873461443",
    "purpose": "entry.1063838522",
}

categories = [
    "Miscellaneous", "Dining", "Bills",
    "Grocery and disposables", "Gas",
    "Buying something", "Entertainments",
    "Beauty products",
]

banks = [
    "Sber", "Tinkoff", "Alpha",  # russian
    "Chase", "AmEx", "Capital One", "Discover"  # american credit cards
    "TD Bank", "BofA",  # american debit cards
    "BNB", "Statusbank",  # belarus
]

# Example
form_data = {
    "entry.1441644747": "5.86",
    "entry.767764842": "Grocery and disposables",
    "entry.1727782915": "8170",
    "entry.412290270": "Tinkoff",
    "entry.873461443": "Yarik",
    "entry.1063838522": "Grocery Samokat",
}

user_agent = {
    "Referer": form_view_url,
    "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"
}

r = requests.post(form_response_url, data=form_data, headers=user_agent)
