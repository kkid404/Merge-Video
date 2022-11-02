from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards import start_kb
from loader import dp

# Exiting the state machine
@dp.message_handler(Text(equals='Back'), state="*")
async def cancel_handlers(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Okey!", reply_markup=start_kb())

@dp.message_handler(text="back", state=None)
async def command_youtube(message: types.Message):
    await bot.send_message(message.from_user.id, "Okey!", reply_markup=start_kb())