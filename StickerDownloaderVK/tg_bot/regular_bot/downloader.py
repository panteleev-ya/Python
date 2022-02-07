import os
import requests
from pathlib import Path


def download_images_from_links(urls_filename, directory="", file_format=".png"):
    urls = open(urls_filename, "r").readlines()
    img_ind = 0

    if directory:
        # If directory doesn't exist - make it
        if not Path(directory).is_dir():
            os.mkdir(directory)
        directory += "/"

    for link in urls:
        img_ind += 1
        req = requests.get(link[:-1], allow_redirects=True)
        open(f"{directory}sticker_{img_ind}{file_format}", "wb").write(req.content)
