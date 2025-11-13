import discord
import globals

async def run(message: discord.Message, args: list[str], client: discord.Client = None):
    files = globals.get_all_files()

    if len(files) == 0:
        return await message.channel.send("theres no files, try uploading something!")
    
    depth = 1
    if len(args) != 0:
        depth = int(args[0])

    to_send = sorted(files, key=lambda f: f.time_uploaded)[-depth :]
    to_send.reverse()

    for file in to_send:
        async with message.channel.typing():
            await message.channel.send(f"filename: {file.name_with_ext} | uploader: {file.owner.discord_user.display_name} ({file.owner.name})", file=discord.File(file.path))