import os
import requests
from pathlib import Path


def download_images_from_list(urls, directory="", file_format=".png"):
    img_id = 0

    if directory:
        # If directory doesn't exist - make it
        if not Path(directory).is_dir():
            os.mkdir(directory)
        directory += "/"

    for link in urls:
        img_id += 1
        req = requests.get(link, allow_redirects=True)
        open(f"{directory}Sticker_{img_id}{file_format}", "wb").write(req.content)
