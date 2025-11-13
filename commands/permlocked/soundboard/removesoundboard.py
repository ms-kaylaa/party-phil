import discord
import globals

from classes.uploads.file import File

async def run(message: discord.Message, args: list[str], client: discord.Client = None):
    user = globals.get_user_from_id(message.author.id)

    if not user.has_permission("PLAY_SOUNDBOARD"): return

    filename = " ".join(args)
    
    for file in user.soundboard_files:
        if file.name_with_ext == filename or file.name == filename:
            file.delete()
            return await message.channel.send("successfully deleted soundboard")
    
    await message.channel.send("i could not find a soundboard with that name!")