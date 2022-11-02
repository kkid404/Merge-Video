from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# Start keyboard
def start_kb():
    Youtube = KeyboardButton("merge youtube")
    Photos = KeyboardButton("merge google photos")
    Drive = KeyboardButton("merge google drive")
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(Youtube, Photos, Drive)
    return keyboard

# Youtube keyboard
def youtube_kb():
    Links = KeyboardButton("merge links from youtube")
    Playlist = KeyboardButton("merge playlist")
    back = KeyboardButton("back")
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(Links, Playlist, back)
    return keyboard

# Google drive keyboard
def drive_kb():
    links = KeyboardButton("merge links from google drive")
    folders = KeyboardButton("merge folders")
    back = KeyboardButton("back")
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(links, folders, back)
    return keyboard

def photos_kb():
    links = KeyboardButton("merge links from google photos")
    albums = KeyboardButton("merge albums")
    back = KeyboardButton("back")
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(links, albums, back)
    return keyboard

def back_kb():
    back = KeyboardButton("Back")
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(back)
    return keyboard

def pay_kb():
    keyboard = InlineKeyboardMarkup(row_width=1)
    yes = InlineKeyboardButton("Yes", callback_data="pay")
    no = InlineKeyboardButton("No", callback_data="no_pay")
    keyboard.add(yes, no)
    return keyboard


def chek_kb(isUrl=True, url="", bill=""):
    payMenu = InlineKeyboardMarkup(row_width=2)
    if isUrl:
        btnUrlQiwi = InlineKeyboardButton("Pay", url=url)
        payMenu.add(btnUrlQiwi)
    chek_pay = InlineKeyboardButton(
        "Check payment", callback_data="chek_"+bill)
    quit = InlineKeyboardButton("Cancel my request", callback_data="quit")
    payMenu.insert(chek_pay).add(quit)
    return payMenu
