# HEXOSE WAS HERE!! I WAS! I WAS HERE!!

import discord
import random

from utils import imageutil

async def run(message: discord.Message, args: list[str], client: discord.Client = None):
    dude = "lady"
    
    file = imageutil.recolor(dude, ["#C6C0B3", "#583D5F", "#F3E0CB", "#3F7270", "#2C3F3E", "#BBC9D0", "#35454D"])
    await message.reply("Here's your random lady!", file=discord.File(file), mention_author=False)