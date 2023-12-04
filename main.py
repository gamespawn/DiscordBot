import discord
import os
# load our local env so we dont have the token in public
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
intents = discord.Intents.all()

client = commands.Bot(command_prefix='!',intents=intents)

# Load cogs
initial_extensions = ['music']  # Add more cogs as needed



@client.event  # check if bot is ready
async def on_ready():
    for extension in initial_extensions:
        await client.load_extension(extension)
        print(f'Loaded extension: {extension}')
    print('Bot online')


client.run(os.getenv('DISCORD_BOT_TOKEN'))

