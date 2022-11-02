from loader import app

from bs4 import BeautifulSoup
import requests
import re
import os

@app.post('/g_photos_download')
def g_photos_download(urls: list):
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
            
            response_download_link = requests.get(url=downloadlink)
            name = re.search(r'filename="(.+)"', response_download_link.headers['Content-Disposition'])
            if name:
                filename = name.group(1)
            else:
                filename = url.split('/')

                if len(filename[-1]) != 0:
                    filename = filename[-1]
                else:
                    filename = filename[-2]
            with open(filename, "wb") as file:
                file.write(response_download_link.content)
            file_size = os.stat(filename).st_size
            videos.append(os.path.abspath(filename))
            size.append(file_size)
            filename, file_extension = os.path.splitext(filename)
            ext.append(file_extension)   
        except KeyError:
            for link in videos:
                os.remove(link)
            return "Incorrect link"
    # for format in ext:
    #     if format != ".mp4" or format != ".MP4":
    #         for link in videos:
    #             os.remove(link)
    #         return "One or more files are not video"   
    try:
        return {"videos": videos, "size": sum(size) / 1000000}
    except Exception as ex:
        return ex