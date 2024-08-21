import datetime
import discord
from discord.ext import commands, tasks

utc = datetime.timezone.utc

# Specify the time when the task should run (using UTC timezone)
time = datetime.time(hour=2, minute=15, tzinfo=utc)

class SchedulerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_send.start()

    def cog_unload(self):
        self.message_send.cancel()

    @tasks.loop(time=time)
    async def message_send(self):
        channel = self.bot.get_channel(1275539716992925770)
        if channel:
            await channel.send("Good night! Make sure to go to sleep early, and get enough sleep!")
            print("Good night message sent")
        else:
            print("Channel not found")

    @message_send.before_loop
    async def before_message_send_task(self):
        await self.bot.wait_until_ready()

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(SchedulerCog(bot))