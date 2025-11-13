import discord
import globals

from classes.uploads.file import File

async def run(message: discord.Message, args: list[str], client: discord.Client = None):
    filename = " ".join(args)
    concatted:list[File] = []
    for file in globals.get_all_files():
        wildcard = file.name == filename and not "." in filename
        exact = file.name_with_ext == filename
        if wildcard or exact:
            concatted.append(file)

    if len(concatted) == 0:
        return await message.channel.send("no files found with that name!")
    elif len(concatted) != 1:
        await message.channel.send("i found multiple uploads with that name!")
    
    for file in concatted:
        async with message.channel.typing():
            await message.channel.send(f"filename: {file.name_with_ext} | uploader: {file.owner.discord_user.display_name} ({file.owner.name})", file=discord.File(file.path))