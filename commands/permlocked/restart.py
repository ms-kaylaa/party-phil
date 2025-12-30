import discord

import globals

import os
import threading

async def run(message: discord.Message, args, client: discord.Client):
    if not globals.get_user_from_id(message.author.id).has_permission("EXEC"):
        print("denied")
        return
    
    def run():
        os.system("python main.py")

    threading.Thread(target=run).start()
    await message.channel.send("Killing this instance")
    client.close()
    exit()