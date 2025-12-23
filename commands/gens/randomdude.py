import discord
import random

from utils import imageutil

async def run(message: discord.Message, args: list[str], client: discord.Client = None):
    dude = "dude"
    if random.randint(0, 24) == 0:
        dude = "realdude"
    
    file = imageutil.recolor(dude, ["#EED6C4", "#8D97C2", "#473E38", "#D7799C", "#653662", "#5F5492", "#353344"])
    await message.reply("Here's your random dude!", file=discord.File(file), mention_author=False)