from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def start_kb_admin():
    Youtube = KeyboardButton("merge youtube[Admin]")
    Photos = KeyboardButton("merge google photos[Admin]")
    Drive = KeyboardButton("merge google drive[Admin]")
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(Youtube, Photos, Drive)
    return keyboard

def youtube_kb_admin():
    playlist = KeyboardButton("merge playlist[Admin]")
    link = KeyboardButton("merge links from youtube[Admin]")
    back = KeyboardButton("back")
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(link, playlist, back)
    return keyboard

# Google drive keyboard
def drive_kb_admin():
    links = KeyboardButton("merge links from google drive[Admin]")
    folders = KeyboardButton("merge folders[Admin]")
    back = KeyboardButton("back")
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(links, folders, back)
    return keyboard

def photos_kb():
    links = KeyboardButton("merge links from google photos[Admin]")
    albums = KeyboardButton("merge albums[Admin]")
    back = KeyboardButton("back")
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(links, albums, back)
    return keyboard


def yes_no():
    keyboard = InlineKeyboardMarkup(row_width=1)
    yes = InlineKeyboardButton("Yes", callback_data="yes")
    no = InlineKeyboardButton("No", callback_data="no")
    keyboard.add(yes, no)
    return keyboard
