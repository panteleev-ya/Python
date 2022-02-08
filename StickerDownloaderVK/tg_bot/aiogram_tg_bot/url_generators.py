def generate_urls_from_range(id_start, id_end, size=512, filename="urls.txt", param=1, url="https://vk.com/sticker/"):
    urls = []
    for i in range(id_start, id_end + 1):
        urls.append(f"{url}{param}-{i}-{size}")
    return urls


def generate_urls_from_list(id_list, size=512, filename="urls.txt", param=1, url="https://vk.com/sticker/"):
    urls = []
    for i in id_list:
        urls.append(f"{url}{param}-{i}-{size}")
    return urls
