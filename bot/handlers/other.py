from aiogram import types

from loader import bot, dp, AGENT

# Forwarding video from an agent
@dp.message_handler(content_types="video")
async def out_video(message: types.Message):
    if message.chat.id == int(AGENT):
        video = message.video.file_id
        id = message.caption
        await bot.send_video(id, video)
