from aiogram.dispatcher.filters.state import State, StatesGroup

class StoragePlaylist(StatesGroup):
    playlist = State()

class StorageLink(StatesGroup):
    links = State()

class StorageGPhotosLink(StatesGroup):
    links = State()

class StorageGDriveLink(StatesGroup):
    links = State()

class StorageGFoldersLink(StatesGroup):
    links = State()

class StorageGAlbumsLink(StatesGroup):
    links = State()

