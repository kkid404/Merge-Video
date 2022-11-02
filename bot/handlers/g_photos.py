from aiogram import types
from aiogram.dispatcher import FSMContext

from states import VideoStorage, StorageGPhotosLink
from keyboards import start_kb, back_kb, pay_kb, chek_kb, youtube_kb, drive_kb, photos_kb
from functions import summary, delete_videos, get_g_photos
from loader import bot, dp
from loader import ADMIN

# Get a link from google photos
@dp.message_handler(text="merge google photos", state=None)
async def g_photo_links_read(message: types.Message):
    await bot.send_message(
        message.chat.id, 
        "Choose what you want to merge links or albums",
        reply_markup=photos_kb()
        )


# Get a google photos links
@dp.message_handler(text="merge links from google photos", state=None)
async def folders(message: types.Message):
    await bot.send_message(
        message.from_user.id, 
        "Send me links to folders that need to be merge.\n"
        "Each link must be on a new line", 
        reply_markup=back_kb()
        )
    await StorageGPhotosLink.links.set()
    
# Download and process video
@dp.message_handler(state=[StorageGPhotosLink.links, VideoStorage])
async def g_photo_input_links(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['links'] = message.text.split('\n')
        links = data["links"]

    if len(links) < 2:
        await bot.send_message(
            message.chat.id, 
            "You can merge at least two videos.", 
            reply_markup=start_kb()
            )
        await state.finish()

    else:
        try:
            await bot.send_message(
                message.chat.id, 
                "Videos received.\nStarting processing...", 
                reply_markup=start_kb()
                )
            
            videos = await get_g_photos(links)
            video = videos["videos"]
            price = await summary(videos["size"])
            
            if price >= 1:  # Spam payment protection
                len_v = len(video)
                size_v = videos["size"]
                await VideoStorage.price.set()
                await VideoStorage.user_id.set()
                await VideoStorage.videos.set()
                async with state.proxy() as data:
                    data["price"] = price
                    data["user_id"] = message.chat.id
                    data["videos"] = video
                await bot.send_message(
                    message.chat.id,
                    f"You want to edit <b>{len_v} video.</b>\n"
                    f"Total weight: <b>{int(size_v)} MB.</b>\n"
                    f"Installation cost: <b>{price} RUB</b>\n"
                    f"Want to pay and continue?", 
                    reply_markup=pay_kb()
                    )
            
            else:
                await bot.send_message(
                    message.chat.id, 
                    "The price of the video is too low", 
                    reply_markup=start_kb()
                    )
                await delete_videos(video)
                await state.finish()
        
        except Exception as ex:
            await bot.send_message(
                message.chat.id, 
                "Video processing error", 
                reply_markup=start_kb()
                )
            print(ex)
            await state.finish()