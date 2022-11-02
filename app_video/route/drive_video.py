from loader import app
import gdown
import os
from random import randint

@app.post('/drive_video')
def download_video_drive(urls: list):
    videos = []
    size = []
    for url in urls:
        id = url.split("/")[5]
        file = gdown.download(id=id, quiet=False)
        filename, file_extension = os.path.splitext(file)
        file_states = os.stat(file)
        size.append(file_states.st_size)
        videos.append(os.path.abspath(file))
        # if file_extension != ".mp4":
            # try:
            #     for video in videos:
            #         os.remove(video)
            # except:
            #     pass
            # return "File are not video"
    try:
        return {"videos": videos, "size": sum(size) / 1000000}
    except Exception as ex:
        return ex