from random import randint


from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from states import StorageLink, VideoStorage
from keyboards import start_kb, pay_kb, youtube_kb, back_kb
from functions import get_videos, summary
from loader import bot, dp

@dp.message_handler(text="merge youtube", state=None)
async def command_youtube(message: types.Message):
    await bot.send_message(
        message.from_user.id, 
        "Choose what you want to merge links or playlists", 
        reply_markup=youtube_kb()
        )

# Get a link from youtube
@dp.message_handler(text="merge links from youtube", state=None)
async def yt_links_read(message: types.Message):
    await bot.send_message(
        message.chat.id, 
        "Send me links to videos "
        "from youtube that need to be merge.\n"
        "Each link must be on a new line\nFor example:\n"
        "https://youtube.com/video1\nhttps://youtube.com/video2",
        reply_markup=back_kb()
        )
    await StorageLink.links.set()

# Download and process video
@dp.message_handler(state=[StorageLink.links, VideoStorage])
async def yt_input_links(message: types.Message, state: FSMContext):
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

            videos = await get_videos(links)
            video = videos["videos"]
            price = await summary(videos["size"])
            len_v = len(video)
            size_v = videos["size"]
            await VideoStorage.price.set()
            await VideoStorage.user_id.set()
            await VideoStorage.videos.set()
            async with state.proxy() as data:
                data["price"] = price
                data["user_id"] = message.chat.id
                data["videos"] = videos["videos"]
 
            await bot.send_message(message.chat.id,
                f"You want to edit <b>{len_v} video.</b>\n"
                f"Total weight: <b>{int(size_v)} MB.</b>\n"
                f"Installation cost: <b>{price} RUB</b>\n"
                "Want to pay and continue?", 
                reply_markup=pay_kb()
                )

        except Exception as ex:
            await bot.send_message(
                message.chat.id, 
                "Video processing error", 
                reply_markup=start_kb()
                )
            print(ex)
            await state.finish()