import discord
from discord import app_commands
from discord.ext import commands
from keys import discord_channel_id, discord_server_id

DISCORD_SERVER_ID = discord_server_id

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Responds with pong")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("pong")

    @app_commands.command(name="sync", description="To safely sync new commands to prevent rate limit.")
    @commands.is_owner()
    async def sync(self, interaction: discord.Interaction, guild_id: int = None):
        if guild_id:
            guild = discord.Object(id=guild_id)
            self.bot.tree.copy_global_to(guild=guild)
            await self.bot.tree.sync(guild=guild)
            await interaction.response.send_message(f"Commands synced to guild {guild_id}", ephemeral=True)
        else:
            await self.bot.tree.sync()
            await interaction.response.send_message("Commands synced globally", ephemeral=True)

    @sync.error
    async def sync_error(self, interaction: discord.Interaction, error):
        if isinstance(error, commands.NotOwner):
            await interaction.response.send_message("You are not the owner!", ephemeral=True)
    
    @commands.Cog.listener()
    async def on_ready(self):
        try:
            # Ensure the /sync command is available globally after the bot is ready
            await self.bot.tree.sync()
            print("Commands synced globally")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

async def setup(bot):
    await bot.add_cog(BotCommands(bot))