filename = "baron_simon_urls.txt"
id_start = 58821
id_end = 58868
param = 1
size = 512
url = "https://vk.com/sticker/"

file = open(filename, "w")
for i in range(id_start, id_end + 1):
    file.write(url + f"{param}-{i}-{size}\n")
file.close()
