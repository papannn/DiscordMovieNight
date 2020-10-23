import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

def check_roles(user_roles: list) -> bool:
    for role in user_roles:
        if role.name == 'Movie Watcher':
            return True
    return False

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

        mention_person = mentions[0]
        user_roles = mention_person.roles
        
        if not check_roles(user_roles):
            await message.channel.send("This person doesn't have \"Movie Watcher\" role")
            return


client.run(TOKEN)