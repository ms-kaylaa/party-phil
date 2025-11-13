import discord
import globals

async def run(message: discord.Message, args: list[str], client: discord.Client = None):
    user = globals.get_user_from_id(message.author.id)

    if user.has_permission("GRANT_PERMISSIONS"):
        user.inc_property("philcoin", int(args[0]) if (len(args) > 0) else 20)
        await message.channel.send(f"done! you now have {user.get_property("philcoin")} philcoin!")