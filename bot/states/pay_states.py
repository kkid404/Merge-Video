from aiogram.dispatcher.filters.state import State, StatesGroup

class BillStorage(StatesGroup):
    bill = State()