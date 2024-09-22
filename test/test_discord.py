import discord

TOKEN = 'mytoken'
CHANNEL_ID = '1221998721693388851'

class MyClient(discord.Client):
    async def on_ready(self):
        channel = self.get_channel(int(CHANNEL_ID))
        await channel.send('Hello World')
 
 
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)