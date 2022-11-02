from aiogram import types
from aiogram.dispatcher import FSMContext

from states import VideoStorage, StorageGAlbumsLink
from keyboards import start_kb, back_kb, pay_kb
from functions import summary, delete_videos, get_g_albums
from loader import bot, dp

# Get a albums
@dp.message_handler(text="merge albums", state=None)
async def folders(message: types.Message):
    await bot.send_message(
        message.from_user.id, 
        "Send me links to albums that need to be merge.\n"
        "Each link must be on a new line", 
        reply_markup=back_kb()
        )
    await StorageGAlbumsLink.links.set()

# Google photos album processing
@dp.message_handler(state=[StorageGAlbumsLink.links, VideoStorage])
async def input_playlist(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["links"] = message.text.split('\n')
        album = data["links"]

    try:
        await bot.send_message(
            message.chat.id, 
            "Albums received.\nStarting processing...",
            reply_markup = start_kb()
            )
        video = await get_g_albums(album)
        price = await summary(video["size"])

        if price >= 1:  # Protection against spam payments
            len_v = len(video["videos"])
            size_v = video["size"]
            await state.finish()

            await VideoStorage.price.set()
            await VideoStorage.user_id.set()
            await VideoStorage.videos.set()

            async with state.proxy() as data:
                data["price"] = price
                data["user_id"] = message.chat.id
                data["videos"] = video["videos"]

            await bot.send_message(message.chat.id,
                f"You want to edit <b>{len_v} video.</b>\n"
                f"Total weight: <b>{int(size_v)} MB.</b>\n"
                f"Installation cost: <b>{price} RUB</b>\n"
                "Want to pay and continue?", 
                reply_markup=pay_kb()
                )
        else:
            await bot.send_message(
                message.chat.id, 
                "The price of the video is too low", 
                reply_markup=start_kb()
                )
            await delete_videos(video["videos"])
            await state.finish()
    
    except Exception as ex:
        await bot.send_message(
            message.chat.id, 
            "You didn't send a albums.", 
            reply_markup=start_kb())
        print(ex)
        await state.finish()