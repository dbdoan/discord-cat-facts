import asyncio
import datetime
import discord
from discord.ext import commands, tasks
import math
import dotenv
import random
import requests
import pandas
import os
import sys

# /////////// /////////// ///////////
os.system('clear')

dotenv.load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    print("No bot token has been set.")
    sys.exit(1)
else:
    print("Bot token has been set.")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Load the Cog
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def load_cogs():
    await bot.load_extension("message_scheduler")

async def main():
    await load_cogs()
    await bot.start(DISCORD_BOT_TOKEN)

# Run the bot using asyncio.run()
if __name__ == "__main__":
    asyncio.run(main())