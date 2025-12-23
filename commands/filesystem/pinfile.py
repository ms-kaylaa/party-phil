import discord
import globals

from utils.fileutil import search_file

async def run(message: discord.Message, args: list[str], client: discord.Client = None):
    if len(args) == 0:
        return await message.channel.send("you need to specify a file to pin/unpin!")
    
    user = globals.get_user_from_id(message.author.id)
    filename = " ".join(args)

    files = search_file(filename, user)

    if len(files) == 0:
        return await message.channel.send("you have no files named that!")
    if len(files) > 1:
        return await message.channel.send("you have multiple files named that! please specify the extension!")
    
    file = files[0]

    if file.get_metadata("pinned"):
        file.set_metadata("pinned", False)
        await message.channel.send(f"unpinned {file.name_with_ext}!")
    else:
        file.set_metadata("pinned", True)
        await message.channel.send(f"pinned {file.name_with_ext}!")