from schemas import Video
from pytube import YouTube
from loader import app
from pytube.helpers import safe_filename
import os
from urllib.error import HTTPError

# Video download from youtube function
@app.post('/video')
def download_video_yt(item: Video):
    videos = []
    size = []
    links = item.link
    for l in links:
        yt = YouTube(l)
        try:
            stream = yt.streams.filter(progressive=True, res="720p")[0]
            stream.download()
            name = f'{safe_filename(yt.title)}.mp4'
            videos.append(name)
            file_states = os.stat(name)
            size.append(file_states.st_size)
        except IndexError:
            stream = yt.streams.filter(progressive=True)[1]
            stream.download()
            name = f'{safe_filename(yt.title)}.mp4'
            videos.append(name)
            file_states = os.stat(name)
            size.append(file_states.st_size)
        except HTTPError:
            continue

    try:
        return {"videos": videos, "size": sum(size) / 1000000}
    except Exception as ex:
        return ex