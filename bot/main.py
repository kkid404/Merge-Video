import os
import logging

from aiogram.utils import executor

import handlers
from loader import dp

# in aiohttp.client changed DEFAULT_TIMEOUT from 5 * 60 to 800 * 60, time in minutes
# made it so that the timeout does not end before the video function works
# API token needs to be changed every half a year


async def on_start(event):
    print("Bot has started")
    logging.basicConfig(level=logging.ERROR, filename="log.txt")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)
