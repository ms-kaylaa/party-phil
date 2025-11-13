import discord
import globals

async def run(message: discord.Message, args: list[str], client: discord.Client = None):
    authoruser = globals.get_user_from_id(message.author.id)
    if not authoruser.has_permission("GRANT_PERMISSIONS"):
        return # nope

    username = args[0]
    perm = args[1].upper()

    user = globals.get_user_from_name(username)
    if user == None:
        return await message.channel.send(f"{username} is not a valid User!")

    user.grant_permission(perm)
    await message.channel.send(f"granted {user.discord_user.display_name} permission {perm}")