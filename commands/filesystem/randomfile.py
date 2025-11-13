import discord
import globals

from classes.uploads.file import File

import random

async def gather_files(filter:bool, filter_list:list[str]=None, message:discord.Message=None):
    concatted:list[File] = []

    # to keep track of which users have and havent been accounted for
    skipped_users = []
    if filter:
        skipped_users = filter_list

    for user in globals.users:
        if filter:
            if not user.name in filter_list:
                continue
            else:
                if user.name in skipped_users:
                    skipped_users.remove(user.name)

        concatted += user.files

    if filter and len(concatted) == 0:
        await message.channel.send("none of the provided users were valid!")
        return await gather_files(False)
    
    return [concatted, skipped_users]

async def run(message: discord.Message, args: list[str], client: discord.Client = None):
    filter = len(args) != 0
    
    ret = await gather_files(filter, args, message)
    file_list:list[File] = ret[0]
    skipped_users = ret[1]
    print(skipped_users)

    if len(file_list) == 0:
        return await message.channel.send("theres no files, try uploading something!")
    if len(skipped_users) > 0:
        await message.channel.send(f"the following users were invalid and skipped: {', '.join(skipped_users)}")

    file = random.choice(file_list)

    async with message.channel.typing():
        await message.channel.send(f"filename: {file.name_with_ext} | uploader: {file.owner.discord_user.display_name} ({file.owner.name})", file=discord.File(file.path))