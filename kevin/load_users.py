import discord

import globals
from classes.userstuff.user import User

import os

async def on_ready(client:discord.Client):
    globals.users = []
    for id in os.listdir(globals.USER_DIR):
        try:
            user = User.from_id(int(id))
            globals.users.append(user)
            print(f"loaded user {user.name}")
        except Exception as e:
            print(f"failed to load user {id}: {e}")

#async def on_exit(client:discord.Client):
    #for user in globals.users:
        #user.save()