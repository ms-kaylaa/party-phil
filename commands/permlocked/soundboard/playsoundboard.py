import discord
import globals

import asyncio
import pygame

from classes.uploads.file import File

pygame.mixer.init()

async def run(message: discord.Message, args: list[str], client: discord.Client = None):
    user = globals.get_user_from_id(message.author.id)

    if not user.has_permission("PLAY_SOUNDBOARD"): return

    filename = " ".join(args)

    # reference other user's soundboards
    if ":" in filename:
        filename_split = filename.split(":")
        user = globals.get_user_from_name(filename_split.pop(0))
        filename = ":".join(filename_split)

    for file in user.soundboard_files:
        if file.name == filename or file.name_with_ext == filename:
            sound = pygame.mixer.Sound(file.path)
            sound.set_volume(0.75)
            sound.play()
            print(f"playing soundboard: {file.name_with_ext}")

            await message.add_reaction("👍")

            def check(reaction:discord.Reaction, duser):
                idcheck = reaction.message.id == message.id
                emojicheck = str(reaction.emoji) == "👎"

                #user = globals.get_user_from_id(duser.id)

                return idcheck and emojicheck

            try:
                await client.wait_for('reaction_add', timeout=sound.get_length(), check=check)
            except asyncio.TimeoutError:
                print("no reaction in time haha")
            else:
                sound.stop()
                await message.remove_reaction("👍", message.guild.me)
                print("stopped sound because reaction")
            