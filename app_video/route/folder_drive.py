import os
import gdown
from loader import app

@app.post('/drive_folder')
def download_folder_drive(urls: list):
    for url in urls:
        videos = gdown.download_folder(url, quiet=True, use_cookies=False)
        size = []
        ext = []
        for video in videos:
            file_states = os.stat(video)
            filename, file_extension = os.path.splitext(video)
            size.append(file_states.st_size)
            ext.append(file_extension)
        # for format in ext:
        #     if format != ".mp4":
        #         for link in videos:
        #             os.remove(link)
        #         return "One or more files are not video"
    try:
        return {"videos": videos, "size": sum(size) / 1000000}
    except Exception as ex:
        return ex


