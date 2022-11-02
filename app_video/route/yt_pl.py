from pytube import YouTube, Playlist
from schemas import PlayList
from pytube.helpers import safe_filename
from urllib.error import HTTPError
from loader import app
import os

# Playlist download functionzz
@app.post("/playlist")
def download_playlist_yt(item: PlayList):
    videos = []
    size = []
    for video in item.link:
        pl = Playlist(video)
        links = [i for i in pl]
        for l in links:
            try:
                yt = YouTube(l)
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
                file_states = os.stat(name).st_size
                size.append(file_states)
            except HTTPError:
                continue

    try:
        return {"videos": videos, "size": sum(size) / 1000000}
    except Exception as ex:
        return ex