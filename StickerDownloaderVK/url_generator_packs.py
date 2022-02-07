filename = "ura_urls.txt"
id_start = 52691
id_end = 52691
param = 1
size = 512
url = "https://vk.com/sticker/"

file = open(filename, "w")
for i in range(id_start, id_end + 1):
    file.write(url + f"{param}-{i}-{size}\n")
file.close()
