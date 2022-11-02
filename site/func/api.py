import aiohttp

# API-запрос на скачивание плейлистов
async def get_playlist(playlist: list):
    async with aiohttp.ClientSession() as session:
        async with session.post("http://127.0.0.1:8080/playlist", json={"link": playlist, "Access-Control-Allow-Origin": "*"}) as resp:
            t = await resp.json()
            return t

# API-запрос на скачивание видео
async def get_videos(videos: list):
    async with aiohttp.ClientSession() as session:
        async with session.post("http://127.0.0.1:8080/video", json={"link": videos, "Access-Control-Allow-Origin": "*"}) as resp:
            t = await resp.json()
            return t


# API download video from google drive request
async def get_g_drive_videos(videos: list):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"http://127.0.0.1:8080/drive_video", json=videos) as resp:
            t = await resp.json()
            return t

# API download folders from google drive request
async def get_g_drive_folder(videos: list):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"http://127.0.0.1:8080/drive_folder", json=videos) as resp:
            t = await resp.json()
            return t

# API download video from google photos request
async def get_g_photos(videos: list):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"http://127.0.0.1:8080/g_photos_download", json=videos) as resp:
            t = await resp.json()
            return t

# API download video from google photos request
async def get_g_albums(videos: list):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"http://127.0.0.1:8080/albums", json=videos) as resp:
            t = await resp.json()
            return t

# API-запрос на монтаж видео
async def get_read_video(videos, names):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"http://127.0.0.1:8080/create?names={names}", json=videos) as resp:
            t = await resp.json()
            return t


async def delete_videos(videos):
    async with aiohttp.ClientSession() as session:
        await session.post(f"http://127.0.0.1:8080/delete", json=videos)
