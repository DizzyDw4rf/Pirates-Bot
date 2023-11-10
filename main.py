import asyncio
import os
import discord
from discord.ext import commands
from config import DISCORD_BOT_TOKEN


intents = discord.Intents.all()
client = commands.Bot(command_prefix="*", intents=intents)


@client.event
async def on_ready():
    await client.tree.sync()
    print(f"{client.user.display_name} is online")
    guild_count = len(client.guilds)
    print(f"{client.user} connected to {guild_count} servers.")


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await client.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with client:
        await load()
        await client.start(DISCORD_BOT_TOKEN)


asyncio.run(main())
