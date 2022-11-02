import os
from random import randint

from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards import start_kb
from loader import ADMIN
from loader import dp, bot
from states import AdminStoragePlaylist, AdminStorageLink, AdminStorageGPhotosLink, AdminStorageGDriveLink, AdminStorageGFoldersLink, VideoStorage
from functions import get_videos, get_playlist, summary, bill, get_read_video\
, delete_videos, get_g_drive_videos\
, get_g_drive_folder,get_g_photos
from keyboards import start_kb_admin, youtube_kb_admin, yes_no, drive_kb_admin, back_kb
from client_bot.main import main

# Ответ на команду админ
@dp.message_handler(commands=["admin"], state=None)
async def admin_start(message: types.Message):
    if str(message.from_user.id) in ADMIN:  # проверка на админа
        await bot.send_message(message.from_user.id, "Hi admin!", reply_markup=start_kb_admin())
    else:
        await bot.send_message(message.from_user.id, f"I don't understand what you mean, use the command /start",
                               reply_markup=start_kb())



@dp.message_handler(text="merge youtube[Admin]", state=None)
async def admin_command_youtube(message: types.Message):
    if str(message.from_user.id) in ADMIN:  # проверка на админа
        await bot.send_message(message.from_user.id, "Choose what you want to merge links or playlists", 
        reply_markup=youtube_kb_admin())

# Exiting the state machine
@dp.message_handler(Text(equals='Back'), state="*")
async def cancel_handlers(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Okey!", reply_markup=start_kb())

@dp.message_handler(text="merge google drive[Admin]", state=None)
async def admin_command_drive(message: types.Message):
    if str(message.from_user.id) in ADMIN:  # проверка на админа
        await bot.send_message(message.from_user.id, "Choose what you want to merge links or folders", 
        reply_markup=drive_kb_admin())


# Get a link from google photos
@dp.message_handler(text="merge google photos[Admin]", state=None)
async def admin_g_photo_links_read(message: types.Message):
    if str(message.from_user.id) in ADMIN:  # проверка на админа
        await bot.send_message(message.chat.id, "Send me links to videos that need to be merge.\n\
Each link must be on a new line",
        reply_markup=back_kb())
        await AdminStorageGPhotosLink.links.set()

# Download and process video
@dp.message_handler(state=[AdminStorageGPhotosLink.links, VideoStorage])
async def admin_g_photo_input_links(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMIN:  # проверка на админа
        async with state.proxy() as data:
            data['links'] = message.text.split('\n')
            links = data["links"]
        if len(links) < 2:
            await bot.send_message(message.chat.id, "You can merge at least two videos.", reply_markup=start_kb())
            await state.finish()
        else:
            try:
                await bot.send_message(message.chat.id, "Videos received.\nStarting processing...", reply_markup=start_kb())
                videos = await get_g_photos(links)
                video = videos["videos"]
                len_v = len(video)
                size_v = videos["size"]
                await VideoStorage.user_id.set()
                await VideoStorage.videos.set()
                async with state.proxy() as data:
                    data["user_id"] = message.chat.id
                    data["videos"] = video
                await bot.send_message(message.chat.id, f"""
You want to edit <b>{len_v} video.</b>\n\
Total weight: <b>{int(size_v)} MB.</b>\n\
Want to pay and continue?""", reply_markup=yes_no())
               
            except Exception as ex:
                await bot.send_message(message.chat.id, "Video processing error", reply_markup=start_kb())
                print(ex)
                await state.finish()

# Get a folders
@dp.message_handler(text="merge folders[Admin]", state=None)
async def admin_folders(message: types.Message):
    if str(message.from_user.id) in ADMIN:  # проверка на админа
        await bot.send_message(message.from_user.id, "Send me links to folders that need to be merge.\n\
Each link must be on a new line", reply_markup=back_kb())
        await AdminStorageGFoldersLink.links.set()

# Google drive folders processing
@dp.message_handler(state=[AdminStorageGFoldersLink.links, VideoStorage])
async def admin_input_playlist(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMIN:  # проверка на админа
        async with state.proxy() as data:
            data["links"] = message.text.split('\n')
            folders = data["links"]
        try:
            await bot.send_message(message.chat.id, "Folder received.\nStarting processing...")
            video = await get_g_drive_folder(folders)
            len_v = len(video["videos"])
            size_v = video["size"]
            await state.finish()
            await VideoStorage.user_id.set()
            await VideoStorage.videos.set()
            async with state.proxy() as data:
                data["user_id"] = message.chat.id
                data["videos"] = video["videos"]
            await bot.send_message(message.chat.id, f"""
You want to edit <b>{len_v} video.</b>\n\
Total weight: <b>{int(size_v)} MB.</b>\n\
Want to pay and continue?""", reply_markup=yes_no())
        except Exception as ex:
            await bot.send_message(message.chat.id, "You didn't send a folder.", reply_markup=start_kb())
            print(ex)
            await state.finish()

# Get a playlist
@dp.message_handler(text="merge playlist[Admin]", state=None)
async def admin_playlist(message: types.Message):
    if str(message.from_user.id) in ADMIN:  # проверка на админа
        await bot.send_message(message.from_user.id, "Send me links to playlists that need to be merge.\n\
Each link must be on a new line", reply_markup=back_kb())
        await AdminStoragePlaylist.playlist.set()

# Playlist processing
@dp.message_handler(state=[AdminStoragePlaylist.playlist, VideoStorage])
async def admin_input_playlist(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMIN:  # проверка на админа
        async with state.proxy() as data:
            data["playlist"] = message.text.split('\n')
            pl = data["playlist"]
        try:
            await bot.send_message(message.chat.id, "Playlist received.\nStarting processing...")
            video = await get_playlist(pl)
            len_v = len(video["videos"])
            size_v = video["size"]
            await state.finish()
            await VideoStorage.user_id.set()
            await VideoStorage.videos.set()
            async with state.proxy() as data:
                data["user_id"] = message.chat.id
                data["videos"] = video["videos"]
            await bot.send_message(message.chat.id, f"""
You want to edit <b>{len_v} video.</b>\n\
Total weight: <b>{int(size_v)} MB.</b>\n\
Want to pay and continue?""", reply_markup=yes_no())
        except Exception as ex:
            await bot.send_message(message.chat.id, "You didn't send a playlist.", reply_markup=start_kb())
            print(ex)
            await state.finish()

###
# Get a link from google drive
@dp.message_handler(text="merge links from google drive[Admin]", state=None)
async def admin_links_read(message: types.Message):
    if str(message.from_user.id) in ADMIN:  # проверка на админа
        await bot.send_message(message.chat.id, "Send me links to videos from google drive that need to be merge.\n\
Each link must be on a new line",
                           reply_markup=back_kb())
        await AdminStorageGDriveLink.links.set()

# Download and process video
@dp.message_handler(state=[AdminStorageGDriveLink.links, VideoStorage])
async def admin_input_links(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMIN:  # проверка на админа
        async with state.proxy() as data:
            data['links'] = message.text.split('\n')
            links = data["links"]
        if len(links) < 2:
            await bot.send_message(message.chat.id, "You can merge at least two videos.", reply_markup=start_kb())
            await state.finish()
        else:
            try:
                await bot.send_message(message.chat.id, "Videos received.\nStarting processing...", reply_markup=start_kb())
                videos = await get_g_drive_videos(links)
                video = videos["videos"]

                len_v = len(video)
                size_v = videos["size"]
                await VideoStorage.user_id.set()
                await VideoStorage.videos.set()
                async with state.proxy() as data:
                    data["user_id"] = message.chat.id
                    data["videos"] = video
                await bot.send_message(message.chat.id, f"""
You want to edit <b>{len_v} video.</b>\n\
Total weight: <b>{int(size_v)} MB.</b>\n\
Want to pay and continue?""", reply_markup=yes_no())
            except Exception as ex:
                await bot.send_message(message.chat.id, "Video processing error", reply_markup=start_kb())
                print(ex)
                await state.finish()

###
# Get a link from youtube
@dp.message_handler(text="merge links from youtube[Admin]", state=None)
async def admin_links_read(message: types.Message):
    if str(message.from_user.id) in ADMIN:  # проверка на админа
        await bot.send_message(message.chat.id, "Send me links to videos from youtube that need to be merge.\n\
Each link must be on a new line",
                           reply_markup=back_kb())
        await AdminStorageLink.links.set()

# Download and process video
@dp.message_handler(state=[AdminStorageLink.links, VideoStorage])
async def admin_input_links(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMIN:  # проверка на админа
        async with state.proxy() as data:
            data['links'] = message.text.split('\n')
            links = data["links"]
        if len(links) < 2:
            await bot.send_message(message.chat.id, "You can merge at least two videos.", reply_markup=start_kb())
            await state.finish()
        else:
            try:
                await bot.send_message(message.chat.id, "Videos received.\nStarting processing...", reply_markup=start_kb())
                videos = await get_videos(links)
                video = videos["videos"]

                len_v = len(video)
                size_v = videos["size"]
                await VideoStorage.user_id.set()
                await VideoStorage.videos.set()
                async with state.proxy() as data:
                    data["user_id"] = message.chat.id
                    data["videos"] = video
                await bot.send_message(message.chat.id, f"""
You want to edit <b>{len_v} video.</b>\n\
Total weight: <b>{int(size_v)} MB.</b>\n\
Want to pay and continue?""", reply_markup=yes_no())
            except Exception as ex:
                await bot.send_message(message.chat.id, "Video processing error", reply_markup=start_kb())
                print(ex)
                await state.finish()

@dp.message_handler(text="back", state=None)
async def admin_command_youtube(message: types.Message):
    await bot.send_message(message.from_user.id, "Okey!", reply_markup=start_kb())

@dp.callback_query_handler(text=["yes", "no"], state=[VideoStorage])
async def admin_pay(callback: types.CallbackQuery, state: FSMContext):
    if str(callback.from_user.id) in ADMIN:
        if callback.data == "no":
            await bot.delete_message(callback.from_user.id, callback.message.message_id - 1)
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            async with state.proxy() as data:
                videos = data["videos"]
            await callback.message.answer("Okey!", reply_markup=start_kb())
            await delete_videos(videos)
            await state.finish()
        else:
            async with state.proxy() as data:
                videos = data["videos"]
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            await bot.send_message(callback.from_user.id, "Starting processing...\n\
When it's ready, I'll send the video as a reply message", 
            reply_markup= start_kb())
            name = randint(1, 5000)
            await state.finish()
            video = await get_read_video(videos, name)
            await main(video, str(callback.from_user.id))
            os.remove(video)
