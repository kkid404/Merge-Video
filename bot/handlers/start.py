from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards import start_kb
from loader import bot, dp



# Response to start command
@dp.message_handler(CommandStart())
async def command_start(message: types.Message):
    await bot.send_message(
        message.from_user.id, 
        "Hello!\nI'm a bot for merging videos from YouTube.com\n"
        "Choose what you would like to do by clicking the button below", 
        reply_markup=start_kb()
        )