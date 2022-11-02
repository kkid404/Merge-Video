from aiogram.dispatcher.filters.state import State, StatesGroup

class AdminStoragePlaylist(StatesGroup):
    playlist = State()

class AdminStorageLink(StatesGroup):
    links = State()

class AdminStorageGPhotosLink(StatesGroup):
    links = State()

class AdminStorageGDriveLink(StatesGroup):
    links = State()

class AdminStorageGFoldersLink(StatesGroup):
    links = State()

class AdminStorageGAlbumsLink(StatesGroup):
    links = State()