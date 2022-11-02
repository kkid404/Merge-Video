from concurrent.futures import thread
import os
from random import randint
import queue

from aiogram import types
from aiogram.dispatcher import FSMContext

from states import VideoStorage, BillStorage
from keyboards import start_kb, chek_kb
from functions import bill, chek_bill, get_read_video, delete_videos
from client_bot.main import main
from loader import bot, dp
from loader import ADMIN

class Stack:
    def __init__(self):
        self.elements = []
    def push(self, element):
        self.elements.append(element)
    def pop(self):
        return self.elements.pop()

stack = Stack()

# Proof of payment
@dp.callback_query_handler(text=["pay", "no_pay"], state=[VideoStorage, BillStorage])
async def pay(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "no_pay":
        await bot.delete_message(callback.from_user.id, callback.message.message_id - 1)
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        async with state.proxy() as data:
            videos = data["videos"]
        await callback.message.answer("Okey!", reply_markup=start_kb())
        await delete_videos(videos)
        await state.finish()
    
    else:
        await bot.edit_message_reply_markup(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=None
        )
        async with state.proxy() as data:
            price = data["price"]
            id = data["user_id"]
        chek = bill(price, id)
        await BillStorage.bill.set()
        async with state.proxy() as data:
            data["bill"] = chek
        
        await bot.send_message(
            callback.from_user.id, 
            f"Your payment link:\n{chek.pay_url}"
            "\nLink expires: <b>30 minutes.</b>", 
            reply_markup=chek_kb(url=chek.pay_url, bill=chek.bill_id)
            )
        
        await bot.send_message(
            callback.from_user.id, 
            'When you make a payment, press the "Check payment" button'
            )



# Checking payment status
@dp.callback_query_handler(text_contains="chek_", state=[BillStorage, VideoStorage])
async def chek_pay(callback: types.CallbackQuery, state: FSMContext):
    if str(callback.from_user.id) in ADMIN:  # проверка на админа
        async with state.proxy() as data:
                    videos = data["videos"]
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await bot.send_message(
            callback.from_user.id, 
            "Video paid for!\nStarting processing...\n"
            "When it's ready, I'll send the video as a reply message\n"
            "You can write your questions @merge_video_support_bot", 
            reply_markup= start_kb()
            )
        name = randint(1, 5000)
        await state.finish()
        stack.push(videos)
        for item in stack.elements:
            name = randint(1, 5000)
            video = get_read_video(item, name)
            await main(video, str(callback.from_user.id))
            stack.pop(item)
            os.remove(video)
    
    else:
        async with state.proxy() as data:
            bill = data["bill"]
        chek = chek_bill(bill.bill_id)
        
        if chek == "PAID":
            async with state.proxy() as data:
                videos = data["videos"]
            await bot.delete_message(
                callback.from_user.id, 
                callback.message.message_id
                )
            
            await bot.send_message(
                callback.from_user.id, 
                "Video paid for!\nStarting processing...\n"
                "When it's ready, I'll send the video as a reply message\n"
                "You can write your questions @merge_video_support_bot", 
                reply_markup= start_kb())
            await state.finish()
            stack.push(videos)
            for item in stack.elements:
                name = randint(1, 5000)
                video = await get_read_video(item, name)
                await main(video, str(callback.from_user.id))
                stack.pop(item)
                os.remove(video)

        else:
            await bot.delete_message(
                callback.from_user.id, 
                callback.message.message_id)
            await bot.send_message(
                callback.from_user.id, 
                "Video not paid for!\nYour payment link:\n"
                f"{bill.pay_url}", 
                reply_markup=chek_kb(False, bill=bill.bill_id)
                )

# Exit and cancel payment
@dp.callback_query_handler(text="quit", state="*")
async def quit(callback: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, "Okey!", reply_markup=start_kb())
    async with state.proxy() as data:
        videos = data["videos"]
        await delete_videos(videos)

    await state.finish()