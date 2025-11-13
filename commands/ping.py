import discord

async def run(message: discord.Message, args: list[str], client: discord.Client = None):
    await message.channel.send("pong!")