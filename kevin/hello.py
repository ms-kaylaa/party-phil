import discord

from globals import PREFIX

async def on_message(client:discord.Client, message:discord.Message):
    if message.content.startswith(PREFIX): return
    
    if "<@1141102885472587777>" in message.content:
        await message.channel.send("my name party phil")