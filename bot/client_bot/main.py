from telethon import TelegramClient
import configparser

# Reads the bot token from settings.ini
config = configparser.ConfigParser()
config.read("settings.ini")
API_ID = config["CLIENT"]["API_ID"]
API_HASH = config["CLIENT"]["API_HASH"]
USERNAME = config["CLIENT"]["USERNAME"]
PHONE = config["CLIENT"]["PHONE"]
BOT = config["CLIENT"]["BOT"]


async def main(video, user):
    async with TelegramClient(PHONE, API_ID, API_HASH) as client:
        await client.send_file(BOT, video, caption=user)


if __name__ == '__main__':
    main()
