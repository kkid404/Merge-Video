from aiogram.dispatcher.filters.state import State, StatesGroup

class VideoStorage(StatesGroup):
    price = State()
    user_id = State()
    videos = State()