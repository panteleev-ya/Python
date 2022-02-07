def generate_urls_from_range(id_start, id_end, size=512, filename="urls.txt", param=1, url="https://vk.com/sticker/"):
    url_file = open(filename, "w")
    for i in range(id_start, id_end + 1):
        url_file.write(f"{url}{param}-{i}-{size}\n")
    url_file.close()


def generate_urls_from_list(id_list, size=512, filename="urls.txt", param=1, url="https://vk.com/sticker/"):
    url_file = open(filename, "w")
    for i in id_list:
        url_file.write(f"{url}{param}-{i}-{size}\n")
    url_file.close()
