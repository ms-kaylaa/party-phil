import discord
import globals

from classes.uploads.file import File

async def run(message: discord.Message, args: list[str], client: discord.Client = None):
    user = globals.get_user_from_id(message.author.id)

    # this one needs an extension
    filename = " ".join(args)
    if not "." in filename:
        return await message.channel.send("you need to specify the extension to prevent duplicate deletion!")
    
    for file in user.files:
        if file.name_with_ext == filename:
            file.delete()
            return await message.channel.send("successfully deleted file")
    
    await message.channel.send("i could not find a file with that name!")