import discord
import globals

from classes.uploads.file import File
from classes.userstuff.user import User

async def send_file_formatted(channel:discord.TextChannel, file:File):
    file.inc_metadata("times_gotten", 1)
    async with channel.typing():
        await channel.send(f"filename: {file.name_with_ext} | uploader: {file.owner.discord_user.display_name} ({file.owner.name})", file=discord.File(file.path))

def search_file(name:str, source_user:User = None) -> list[File]:
    concatted:list[File] = []
    
    search_list = None
    if source_user == None:
        search_list = globals.get_all_files()
    else:
        search_list = source_user.files
    
    for file in search_list:
        wildcard = file.name == name and not "." in name
        exact = file.name_with_ext == name
        if wildcard or exact:
            concatted.append(file)

    return concatted

# https://stackoverflow.com/a/59634071
UNITS = {1000: ['KB', 'MB', 'GB'],
            1024: ['KiB', 'MiB', 'GiB']}

def approximate_size(size, use_base_1024=False):
    mult = 1024 if use_base_1024 else 1000
    for unit in UNITS[mult]:
        size = size / mult
        if size < mult:
            return '{0:.3f} {1}'.format(size, unit)