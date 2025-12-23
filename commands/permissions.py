import discord
import globals
from classes.userstuff import permission


async def run(message: discord.Message, args: list[str], client: discord.Client = None):
    user = globals.get_user_from_id(message.author.id)
    permissions = user._permissions
    if len(permissions) == 0:
        return
    await message.channel.send(f"you have perms {", ".join([str(perm) for perm in permissions])}")