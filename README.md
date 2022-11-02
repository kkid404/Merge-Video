# Auto Merge Video 

Auto Merge Video - this is a website and a telegram bot for automatically editing videos from YouTube, Google Drive and Google Photos

Auto Merge Video uses microservice architecture, for it to work, you need to include separately app_video, bot, site

## Telegram bot settings

There is a settings.ini file in the bot folder
In the [BOT] category, you need to specify the bot token with @botfather and the ID of the telegram
account from which files will be sent to the bot

In the [CLIENT] category, you need to specify the API ID, API HASH, username and phone number of the
account from which the video will be sent to the telegram bot.
You can get API ID and API HASH for the client at https://my.telegram.org/auth

CLIENT is needed to bypass telegram restrictions on the size of files that the bot can send.

To connect payments, you must receive a QIWI token https://qiwi.com/p2p-admin/transfers/api
And paste it into [QIWI]

## Site settings

Videos are sent to the mail via google drive, you need to create a new application in google and
upload cleint_secrets.json to the site folder. After the first authorization, it will create token.json
and authorization will take place automatically.

For the correct operation of sending letters to the mail, you need to create an application password
in your google account and write it in the [MAIL] category in settings.ini HOST and PORT I left the default gmail

you also need to duplicate the qiwi token in settings.ini in the site folder

## Library setting 

### Aiohttp
In aiohttp/client.py you need to change DEFAULT_TIMEOUT from 5 * 60 to 800 * 60. If you need more time to process your videos, you can increase the first value. If this is not done, the client parts will not wait for the video after 5 minutes

### Telethon
In Telethon/utils.py values ​​change the file_size in the get_assigned_part_size function to 4194304 for this to work correctly, tedegram premium must be enabled on the agent. If you don't have telegram premium on agent, don't touch this setting