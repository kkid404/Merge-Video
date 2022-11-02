from loader import app
import os

# Delete source function
@app.post('/delete')
def delete(videos: list):
    for video in videos:
        os.remove(video)