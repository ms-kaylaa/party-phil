import discord
import globals
from classes.userstuff import permission


async def run(message: discord.Message, args: list[str], client: discord.Client = None):
    user = globals.get_user_from_id(message.author.id)
    permissions = user._permissions
    list_perms = []
    for i in permissions:
        if type(i) == str:
            list_perms.append(i.lower())
    await message.channel.send(f"you have perms {", ".join(list_perms)}")
