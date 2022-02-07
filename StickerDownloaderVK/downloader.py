import os
import requests
from pathlib import Path

directory = "best_stickers/"
# filename = f"{directory[:-1]}_urls.txt"
filename = f"ura_urls.txt"
_format = ".png"

urls = open(filename, "r").readlines()
ind = 0
dir_name = Path(directory)
if not dir_name.is_dir():
    os.mkdir(directory)
for link in urls:
    ind += 1
    print(link[:-1])
    req = requests.get(link[:-1], allow_redirects=True)
    open(f"{directory}sticker_{ind}{_format}", "wb").write(req.content)
