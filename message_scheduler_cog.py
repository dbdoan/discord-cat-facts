import datetime
from discord.ext import commands, tasks
from keys import discord_channel_id
import pandas
import random
import requests

# /////////// /////////// ///////////
DISCORD_CHANNEL_ID = discord_channel_id

try:
    response = requests.get('https://cat-fact.herokuapp.com/facts')
    response.raise_for_status()
    if response.ok:
        print(f"Status Code: {response.status_code}")
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP Error occurred: {http_err}")
except Exception as err:
    print(f"Error: {err}")

cat_facts_df = pandas.DataFrame(data=response.json())
random_fact_val = random.randint(0, len(cat_facts_df))
# print()

# /////////// /////////// ///////////
# Set time to send scheduled message
utc = datetime.timezone.utc
time = datetime.time(hour=13, minute=43, tzinfo=utc)

# Optional: seconds
# time = datetime.time(hour=13, minute=35, second=45, tzinfo=utc)

class SchedulerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_send.start()

    def cog_unload(self):
        self.message_send.cancel()

    @tasks.loop(time=time)
    async def message_send(self):
        channel = self.bot.get_channel(DISCORD_CHANNEL_ID)
        if channel:
            daily_cat_fact = cat_facts_df['text'][random_fact_val]
            await channel.send(f"Good morning! 🐈\nHere's your daily cat fact to start the day:\n\n```{daily_cat_fact}```")
            print(f"Fact sent at {utc}.")
        else:
            print("Channel not found")

    @message_send.before_loop
    async def before_message_send_task(self):
        await self.bot.wait_until_ready()

# /////////// /////////// ///////////
# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(SchedulerCog(bot))