import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

server_active = {}
users_active = {}
EMOJI_LIST = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

def check_roles(user_roles: list) -> bool:
    for role in user_roles:
        if role.name == 'Movie Watcher':
            return True
    return False

def filter_user_with_movie_watcher_role(user_list, mention_person):
    users = []
    for user in user_list:
        if user == mention_person:
            continue
        for role in user.roles:
            if role.name == 'Movie Watcher':
                users.append(user)
    return users

async def pm_all_user(user_list):
    for user in user_list:
        movie_score = await user.send("How's the movie? Gimme score from 1 to 10")
        for EMOJI in EMOJI_LIST:
            await movie_score.add_reaction(EMOJI)

def add_members_to_active_state(user_list, guild_id, users_active):
    for user in user_list:
        if users_active.get(user.id, None) is not None:
            users_active[user.id]['server_active_count'] += 1
            users_active[user.id]['server_active_list'].append(guild_id)
        else:
            users_active[user.id] = {
                'server_active_count': 1,
                'server_active_list': [guild_id]
            }

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

        user_movie_watcher = filter_user_with_movie_watcher_role(message.guild.members, mention_person)
        
        guild_id = message.guild.id
        server_active[guild_id] = {
            'total_points': 0,
            'total_voters:': 0
        }
        add_members_to_active_state(user_movie_watcher, guild_id, users_active)
        await message.channel.send("Attention Movie Watcher, please check your personal messages")
        await pm_all_user(user_movie_watcher)

@client.event
async def on_reaction_add(reaction, user):
    if client.user != user:
        await user.send("Thank you for voting")

client.run(TOKEN)