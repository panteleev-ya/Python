filename = "best_stickers_urls.txt"
id_arr = [
    2480,
    162,
    126,
    104,
    3135,
    6887,
    14991,
    13614,
    13610,
    13605,
    13627,
    18480,
    6335,
    6353,
    52707,
    58019,
    58031,
    58041,
    58613,
    58621,
    58643,
    50510,
    50532,
    59410,
    61426,
    61454,
    18820
]
param = 1
size = 512
url = "https://vk.com/sticker/"

file = open(filename, "w")
for _id in id_arr:
    file.write(url + f"{param}-{_id}-{size}\n")
file.close()
