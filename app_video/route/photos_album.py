from bs4 import BeautifulSoup
import requests
import re
import os
import zipfile
from random import randint
from loader import app

@app.post('/albums')
def download_albums(urls: list):
    videos = []
    size = []
    ext = []
    for url in urls:
        response = requests.get(url=url)
        soup = BeautifulSoup(response.text, 'html.parser').prettify()
        try:
            downloadlink = str(re.findall(r'https://video-downloads.googleusercontent.com/(.+)",', soup))
            downloadlink = downloadlink.split('"')
            downloadlink = str("https://video-downloads.googleusercontent.com/" + downloadlink[0]).replace("[", "").replace("'", "")
            response_download_link = requests.get(url=downloadlink, stream = True)
            name = f"{randint(1, 1000000)}.zip"
            with open(name, "wb") as c:
                for chunk in response_download_link.iter_content(chunk_size=1024):
                    c.write(chunk)
            fantasy_zip = zipfile.ZipFile(name)
            with fantasy_zip as zip:
                for info in zip.infolist():
                    videos.append(os.path.abspath(info.filename))
                fantasy_zip.extractall()
            os.remove(name)
            for video in videos:
                file_states = os.stat(video)
                size.append(file_states.st_size)
        except KeyError:
            for link in videos:
                os.remove(link)
            return "Incorrect link"
    try:
        return {"videos": videos, "size": sum(size) / 1000000}
    except Exception as ex:
        return ex