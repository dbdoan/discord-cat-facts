import datetime
from discord.ext import commands, tasks
import pandas as pd
import requests

# /////////// /////////// ///////////
def fetch_cat_facts():
    try:
        response = requests.get('https://catfact.ninja/fact?max_length=140')
        response.raise_for_status()
        if response.ok:
            fact = response.json()['fact']
            print(f"Status Code: {response.status_code}")
            return fact
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
    except Exception as err:
        print(f"Error: {err}")
    return None

# /////////// /////////// ///////////
# Set time to send scheduled message [UTC time]
utc = datetime.timezone.utc
time = datetime.time(hour=14, minute=00, tzinfo=utc)

class SchedulerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.csv_file = 'ids.csv'
        self.guild_id = None
        self.channel_id = None

        self.message_send.start()

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.guilds:
            print("Bot is not in any guilds.")
            return
    
        self.guild_id = self.bot.guilds[0].id
        self.load_channel_id()

    def load_channel_id(self):
        self.guild_id = self.bot.guilds[0].id
        df = pd.read_csv(self.csv_file)

        if self.guild_id in df['guild_id'].values:
            self.channel_id = df.loc[df['guild_id'] == self.guild_id, 'channel_id'].values[0]
        else:
            print(f"Guild ID {self.guild_id} not found in CSV.")

    def update_daily_cat_fact(self, fact):
        """Update the CSV file with the daily cat fact for the current guild."""
        try:
            df = pd.read_csv(self.csv_file)
            if self.guild_id in df['guild_id'].values:
                df.loc[df['guild_id'] == self.guild_id, 'daily_cat_fact'] = fact
                df.to_csv(self.csv_file, index=False)
                print("CSV updated with the new daily cat fact.")
            else:
                print(f"Guild ID {self.guild_id} not found in CSV.")
        except (FileNotFoundError, pd.errors.EmptyDataError) as e:
            print(f"Error updating CSV: {e}")

    def cog_unload(self):
        self.message_send.cancel()

    @tasks.loop(time=time)
    async def message_send(self):
        if not self.channel_id:
            print("Channel ID is not set.")
            return
        
        channel = self.bot.get_channel(self.channel_id)
        time_now = datetime.datetime.now()
        formatted_time = time_now.strftime("%I:%M %p")
        if channel:
            daily_cat_fact = fetch_cat_facts() 

            if daily_cat_fact:
                # Send the cat fact to the channel
                await channel.send(f"Good morning! 🐈\nHere's your daily cat fact to start the day:\n\n```{daily_cat_fact}```")
                print(f"Fact sent at {formatted_time}.")

                # Update the CSV with the chosen daily cat fact
                self.update_daily_cat_fact(daily_cat_fact)
            else:
                print("Failed to fetch a cat fact.")
        else:
            print("Channel not found")

    @message_send.before_loop
    async def before_message_send_task(self):
        await self.bot.wait_until_ready()

# /////////// /////////// ///////////
# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(SchedulerCog(bot))