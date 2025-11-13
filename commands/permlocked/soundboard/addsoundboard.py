import discord
import globals

from classes.uploads.file import File

async def run(message: discord.Message, args: list[str], client: discord.Client = None):
    user = globals.get_user_from_id(message.author.id)

    if not user.has_permission("PLAY_SOUNDBOARD"): return

    attach = message.attachments

    if len(attach) == 0:
        return await message.channel.send("you gotta attach an mp3 to upload a soundboard!")
    
    filename = " ".join(args)

    if filename.strip() == "":
        filename = attach[0].filename
    if not "." in filename:
        filename += "." + attach[0].filename.split(".").pop()

    if "/" in filename or "\\" in filename:
        return await message.channel.send("no!")
    if filename in [f.name_with_ext for f in user.soundboard_files]:
        return await message.channel.send(f"you already have a soundboard uploaded with that name! ({filename})")
    if not filename.endswith(".mp3"):
        return await message.channel.send("the uploaded soundboard file must be in mp3 format!")
    
    soundboard_dir = f"{user.user_dir}/soundboard/"
    await attach[0].save(soundboard_dir + filename)

    await message.channel.send("soundboard added!")