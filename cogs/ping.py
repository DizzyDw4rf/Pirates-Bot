import discord
from discord import app_commands
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="ping", description="Show bot's latency")
    async def ping(self, interaction: discord.Interaction):
        bot_latency = round(self.client.latency * 1000)
        await interaction.response.send_message(f"{bot_latency} ms.", ephemeral=True)


async def setup(client):
    await client.add_cog(Ping(client))
