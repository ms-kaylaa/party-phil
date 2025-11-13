import discord
import globals

import os

async def run(message: discord.Message, args: list[str], client: discord.Client = None):
    attach = message.attachments
    if len(attach) == 0:
        return await message.channel.send("you need to attach something to upload something!")

    filename = " ".join(args)
    if "/" in filename or "\\" in filename:
        return await message.channel.send("no!")
    
    user = globals.get_user_from_id(message.author.id)
    file_dir = f"{user.user_dir}/files/"

    if filename.strip() == "":
        filename = attach[0].filename
    if not "." in filename:
        filename += "." + attach[0].filename.split(".").pop()
    if filename in [f.name_with_ext for f in user.files]:
        return await message.channel.send(f"you already uploaded something with that filename ({filename})!")

    await attach[0].save(file_dir + filename)
    await message.delete()
    await message.channel.send(f"saved as {filename}!\nthank you for uploading to party phil! 20 philcoin have been deposited into your ph!balance!")
    user.inc_property("philcoin", 20)