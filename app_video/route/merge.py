from moviepy.editor import VideoFileClip, concatenate_videoclips
from loader import app
import os

# Source merging function
@app.post('/create')
def merge_video(videos: list, names: str):
    r_videos = []
    for video in videos:
        r_v = VideoFileClip(video)
        r_videos.append(r_v)
    try:
        final_clip = concatenate_videoclips(r_videos, method="compose")
        final_clip.write_videofile(f"{names}.mp4")
        try:
            for video in videos:
                os.remove(video)
        except:
            pass
        p = os.path.abspath(f"{names}.mp4")
        return p
    except Exception as ex:
        print("Ничего не вышло :(")
        print(ex)