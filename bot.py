import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    content = message.content
    
    if content.startswith('!friday vote'):
        mentions = message.mentions

        if len(mentions) == 0:
            await message.channel.send("You didn't mention anyone yet!, Please mention someone")
            return
        elif len(mentions) > 1:
            await message.channel.send("Please mention 1 person only!")
            return

client.run(TOKEN)