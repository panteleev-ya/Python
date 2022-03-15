def generate_promo(username):
    promo = "PR-"
    hash_code = str((len(username) ^ hash(username)) % 10000)
    hash_code = '0' * (4 - len(hash_code)) + hash_code
    promo += hash_code
    return promo
