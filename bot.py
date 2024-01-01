# import pyromod.listen
import pyrogram, sys, config
from pyrogram import Client

class Bot(Client):
    def __init__(self):
        super().__init__(
            'scrapBotDoodStream',
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            plugins={
                "root": "plugins"
            },
        )
    async def start(self):
        await super().start()
        botMe = await self.get_me()
        
        if config.CHANNEL_ID:
            try:
                await self.export_chat_invite_link(config.CHANNEL_ID)
            except:
                print(f'Harap periksa kembali ID [ {config.CHANNEL_ID} ] pada CHANNEL_ID')
                print(f'Pastikan bot telah dimasukan kedalam channel dan menjadi admin')
                print('-> Bot terpaksa dihentikan')
                sys.exit()
        if config.CHANNEL_DATABASE:
            try:
                await self.export_chat_invite_link(config.CHANNEL_DATABASE)
            except:
                print(f'Harap periksa kembali ID [ {config.CHANNEL_DATABASE} ] pada CHANNEL_DATABASE')
                print(f'Pastikan bot telah dimasukan kedalam channel dan menjadi admin')
                print('-> Bot terpaksa dihentikan')
                sys.exit()

        self.botUsername = botMe.username
        self.botName = botMe.first_name
        self.botID = botMe.id
        print("")
        print("======== BOT INFO ========")
        print(f"ID\t\t: {self.botID}")
        print(f"Name\t\t: {self.botName}")
        print(f"Username\t: @{self.botUsername}")
        print("==========================")
        print(f"{self.botName.capitalize()} Is running!")
        print("")
    
    async def stop(self):
        await super().stop()
        print(f"{self.botName.capitalize()} Has been stopped!")